from framework.api import task
from framework.utils.shell import shell
from modules.apt import AptSource


@task(
    tags=[
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
        )
    ]
)
def setup():
    pass


@setup.when_check_fails
def _():
    pass
