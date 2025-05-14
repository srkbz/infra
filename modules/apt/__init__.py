from dataclasses import dataclass
from os.path import join, isfile
from hashlib import sha256

from framework.api import task
from framework.runner import runner
from framework.models import Task
from framework.utils.shell import shell
from framework.utils.fs import read_file, remove_all, write_file

import settings

PACKAGES = getattr(settings, "APT_PACKAGES", [])
CACHE_DIR = settings.CACHE_DIR


@dataclass(frozen=True)
class AptPackages:
    packages: list[str]


@dataclass(frozen=True, kw_only=True)
class AptSource:
    arch: str | None
    key: str | None
    url: str
    version: str
    release: str


_cache_dir = join(CACHE_DIR, "apt")
_metapackage_dir = join(_cache_dir, "metapackage")
_metapackage_deb = _metapackage_dir + ".deb"
_debian_dir = join(_metapackage_dir, "DEBIAN")
_control_file = join(_debian_dir, "control")
_installed_control_file = join(_cache_dir, "INSTALLED_CONTROL")


def get_tasks_with_apt_packages() -> list[Task]:
    return [task for task in runner.get_tasks() if task.get_tags(AptPackages)]


def get_tasks_with_apt_sources() -> list[Task]:
    return [task for task in runner.get_tasks() if task.get_tags(AptSource)]


def get_packages() -> list[str]:
    return list(
        dict.fromkeys(
            [
                package
                for task in runner.get_tasks()
                for tag in task.get_tags(AptPackages)
                for package in tag.packages
            ]
            + PACKAGES
        )
    )


def get_sources() -> list[AptSource]:
    return list(
        dict.fromkeys(
            [
                source
                for task in runner.get_tasks()
                for source in task.get_tags(AptSource)
            ]
        )
    )


def build_control_file() -> str:
    packages = get_packages()

    control_lines = [
        "Package: srkbz-infra-metapackage",
        "Version: 0.0.0",
        "Maintainer: Carlos Fdez. Llamas <hello@sirikon.me>",
        "Architecture: all",
        "Description: Metapackage containing all the packages needed",
        *(["Depends: " + ", ".join(packages)] if len(packages) > 0 else []),
    ]
    return "\n".join(control_lines) + "\n"


def setup_sources(*, dry_run=False):
    sources = get_sources()

    list_path = "/etc/apt/sources.list.d/srkbz-infra.list"
    list_content = []

    for source in sources:
        url_hash = sha256()
        url_hash.update(source.url.encode("utf-8"))
        url_hash_digest = url_hash.hexdigest()
        key_path = join("/etc/apt/keyrings/", "srkbz_infra_source_" + url_hash_digest)

        if not isfile(key_path):
            assert not dry_run
            shell("install -m 0755 -d /etc/apt/keyrings")
            shell(
                f"curl -fsSL '{source.url}' -o '{key_path}'",
            )
            shell(f"chmod a+r '{key_path}'")

        line = ["deb"]
        if source.arch is not None or source.key is not None:
            line.append(" [")
            if source.arch is not None:
                line.append("arch=" + source.arch + " ")
            if source.key is not None:
                line.append("signed-by=" + key_path)
            line.append("] ")
        line.append(source.url)
        line.append(" " + source.version)
        line.append(" " + source.release)
        list_content.append("".join(line))

    list_content_text = "\n".join(list_content) + "\n"

    if not isfile(list_path) or read_file(list_path) != list_content_text:
        assert not dry_run
        write_file(list_path, list_content_text)


@task(required_by=[get_tasks_with_apt_sources])
def install_sources():
    setup_sources(dry_run=False)


@install_sources.when_check_fails
def _():
    setup_sources(dry_run=True)


@task(requires=[install_sources], required_by=[get_tasks_with_apt_packages])
def install_packages():
    remove_all(_metapackage_dir)
    control_file_content = build_control_file()
    write_file(_control_file, control_file_content)

    shell(f"dpkg-deb --build '{_metapackage_dir}' '{_metapackage_deb}'")
    shell("apt-get update")
    shell(f"apt-get install -y '{_metapackage_deb}'")
    shell("apt-get autoremove -y")
    write_file(_installed_control_file, control_file_content)


@install_packages.when_check_fails
def _():
    assert read_file(_control_file) == build_control_file()
    assert read_file(_installed_control_file) == build_control_file()
    assert isfile(_metapackage_deb)
