from dataclasses import dataclass
from os import makedirs
from os.path import join

from framework import get_runner, task, shell
from modules.base_dirs import get_base_dirs


def setup_apt():

    cache_dir = join(get_base_dirs().cache_dir, "apt")
    metapackage_dir = join(cache_dir, "metapackage")
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

        try:
            with open(control_file, "r") as f:
                if control == f.read():
                    return
        except FileNotFoundError:
            pass

        yield

        shell(f"rm -rf '{metapackage_dir}'")
        makedirs(debian_dir)
        with open(control_file, "w") as f:
            f.write(control)

        shell(f"dpkg-deb --build '{metapackage_dir}' '{metapackage_dir}.deb'")


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
