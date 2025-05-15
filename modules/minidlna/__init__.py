from framework.api import task
from framework.utils.fs import read_file, write_file
from framework.utils.shell import shell

from modules.apt import AptPackages
from modules.directories import Directory

from .conf_builder import *


def do_setup(*, dry_run: bool):
    conf = build_conf()
    if dry_run:
        assert read_file("/etc/minidlna.conf") == conf
    else:
        write_file("/etc/minidlna.conf", conf)

    if dry_run:
        shell("systemctl status minidlna.service >/dev/null", echo=False)
    else:
        shell("systemctl restart minidlna.service")


@task()
def setup():
    do_setup(dry_run=False)


setup.enabled(lambda: ENABLED)
setup.tags(lambda: [AptPackages(["minidlna"]), Directory(DIRECTORY_ID)])
setup.when_check_fails(lambda: do_setup(dry_run=True))
