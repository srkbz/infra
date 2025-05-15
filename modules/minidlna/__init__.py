from framework.api import task
from framework.utils.fs import read_file, write_file
from framework.utils.shell import shell

from modules.apt import AptPackages
from modules.directories import Directory

from .conf_builder import *


@task()
def setup():
    write_file("/etc/minidlna.conf", build_conf())
    shell("systemctl restart minidlna.service")


setup.enabled(lambda: ENABLED)
setup.tags(lambda: [AptPackages(["minidlna"]), Directory(DIRECTORY_ID)])


@setup.when_check_fails
def _():
    assert read_file("/etc/minidlna.conf") == build_conf()
    shell("systemctl status minidlna.service >/dev/null", echo=False)
