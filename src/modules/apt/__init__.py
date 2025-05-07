from dataclasses import dataclass
from os.path import join, isfile

from framework import get_runner, task
from framework.utils.context import get_context_value
from framework.utils.shell import shell
from framework.utils.fs import read_file, remove_all, write_file
from modules.base_dirs import BaseDirs


def install_apt_packages(packages: list[str]):
    @task(tags=[AptPackages(packages)], title=" ".join(packages))
    def default():
        return
        yield


def setup_apt():

    cache_dir = join(get_context_value(BaseDirs).cache_dir, "apt")
    metapackage_dir = join(cache_dir, "metapackage")
    metapackage_deb = metapackage_dir + ".deb"
    debian_dir = join(metapackage_dir, "DEBIAN")
    control_file = join(debian_dir, "control")

    packages = get_packages()

    @task(required_by=get_tasks_with_apt_packages())
    def install_apt_packages():
        control_lines = [
            "Package: srkbz-infra-metapackage",
            "Version: 0.0.0",
            "Maintainer: Carlos Fdez. Llamas <hello@sirikon.me>",
            "Architecture: all",
            "Description: Metapackage containing all the packages needed",
            *(["Depends: " + ", ".join(packages)] if len(packages) > 0 else []),
        ]
        control = "\n".join(control_lines) + "\n"

        if read_file(control_file) == control and isfile(metapackage_deb):
            return
        yield

        remove_all(metapackage_dir)
        write_file(control_file, control)

        shell(f"dpkg-deb --build '{metapackage_dir}' '{metapackage_deb}'")

    @install_apt_packages.when_check_fails
    def _():
        assert 1 == 1


@dataclass(frozen=True)
class AptPackages:
    packages: list[str]


def get_packages() -> list[str]:
    return list(
        dict.fromkeys(
            [
                package
                for task in get_runner().tasks
                for tag in task.get_tags(AptPackages)
                for package in tag.packages
            ]
        )
    )


def get_tasks_with_apt_packages():
    return [task for task in get_runner().tasks if task.get_tags(AptPackages)]
