from framework.api import task
from framework.utils.shell import shell

from modules import apt


class Config:
    def __init__(self):
        self._enabled = False

    def enable(self):
        if not self._enabled:
            self._enabled = True
            apt.config.add_sources(
                apt.Source(
                    arch=shell(
                        "dpkg --print-architecture", captureStdout=True, echo=False
                    ).stdout.strip(),
                    key="https://download.docker.com/linux/debian/gpg",
                    url="https://download.docker.com/linux/debian",
                    version=shell(
                        '. /etc/os-release && echo "$VERSION_CODENAME"',
                        captureStdout=True,
                        echo=False,
                    ).stdout.strip(),
                    release="stable",
                )
            )
            apt.config.add_packages(
                "docker-ce",
                "docker-ce-cli",
                "containerd.io",
                "docker-buildx-plugin",
                "docker-compose-plugin",
            )


@task(requires=[apt.install_packages])
def setup(dry_run: bool):
    pass
