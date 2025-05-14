from framework.api import task
from framework.utils.shell import shell
from modules.apt import AptSource


@task(
    tags=[
        AptSource(
            arch=shell("dpkg --print-architecture", captureStdout=True).stdout.strip(),
            key="https://download.docker.com/linux/debian/gpg",
            url="https://download.docker.com/linux/debian",
            version=shell(
                '. /etc/os-release && echo "$VERSION_CODENAME"', captureStdout=True
            ).stdout.strip(),
            release="stable",
        )
    ]
)
def setup():
    pass
