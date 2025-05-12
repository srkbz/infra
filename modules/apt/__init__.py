from dataclasses import dataclass
from os.path import join, isfile

from framework.api import task
from framework.runner import runner
from framework.models import Task
from framework.utils.shell import shell
from framework.utils.fs import read_file, remove_all, write_file

from settings import CACHE_DIR, APT_PACKAGES


@dataclass(frozen=True)
class AptPackages:
    packages: list[str]


_cache_dir = join(CACHE_DIR, "apt")
_metapackage_dir = join(_cache_dir, "metapackage")
_metapackage_deb = _metapackage_dir + ".deb"
_debian_dir = join(_metapackage_dir, "DEBIAN")
_control_file = join(_debian_dir, "control")


def get_tasks_with_apt_packages() -> list[Task]:
    return [task for task in runner.get_tasks() if task.get_tags(AptPackages)]


def get_packages() -> list[str]:
    return list(
        dict.fromkeys(
            [
                package
                for task in runner.get_tasks()
                for tag in task.get_tags(AptPackages)
                for package in tag.packages
            ]
            + APT_PACKAGES
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


@task(required_by=[get_tasks_with_apt_packages])
def install_packages():
    remove_all(_metapackage_dir)
    write_file(_control_file, build_control_file())

    shell(f"dpkg-deb --build '{_metapackage_dir}' '{_metapackage_deb}'")


@install_packages.when_check_fails
def _():
    assert read_file(_control_file) == build_control_file()
    assert isfile(_metapackage_deb)
