from framework.api import task
from framework.utils.shell import shell
from modules.apt import AptPackages, AptSource


class Config:
    def __init__(self):
        self._enabled = False

    def enable(self):
        self._enabled = True


config = Config()


@task()
def setup():
    pass


@setup.when_check_fails
def _():
    pass


@setup.enabled
def _():
    return config._enabled


@setup.tags
def _():
    if config._enabled:
        return [
            AptSource(
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
            ),
            AptPackages(
                [
                    "docker-ce",
                    "docker-ce-cli",
                    "containerd.io",
                    "docker-buildx-plugin",
                    "docker-compose-plugin",
                ]
            ),
        ]
    return []
