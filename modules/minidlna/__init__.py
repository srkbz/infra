from os.path import isfile

from framework.api import task
from framework.utils.fs import read_file, write_file
from framework.utils.shell import shell

from modules import apt
from modules.directories import Directory

from .conf_builder import *

if is_enabled():
    apt.config.add_packages("minidlna")

_conf_file = "/etc/minidlna.conf"


def _setup(dry_run: bool):
    conf = build_conf()

    if read_file(_conf_file) != conf:
        assert not dry_run
        write_file(_conf_file, conf)

    if (
        shell(
            "systemctl status minidlna.service >/dev/null", echo=False, check=False
        ).exit_code
        != 0
    ):
        assert not dry_run
        shell("systemctl restart minidlna.service")


def _cleanup(dry_run: bool):
    if isfile(_conf_file):
        assert not dry_run
        shell(f"rm -f '{_conf_file}'")


def _needs_cleanup():
    try:
        _cleanup(dry_run=True)
        return False
    except:
        return True


@task()
def setup(dry_run: bool):
    if is_enabled():
        _setup(dry_run)


setup.enabled(lambda: is_enabled() or _needs_cleanup())
setup.tags(lambda: [Directory(DIRECTORY_ID)])
