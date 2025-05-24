from os.path import isdir, isfile, join, dirname
from os import makedirs

from framework.api import task
from framework.utils.fs import read_file, write_file

from framework.utils.shell import shell
from modules import apt

import settings


ENABLED = getattr(settings, "NOTIFY_ENABLED", False)
TARGET = getattr(settings, "NOTIFY_TARGET", None)
BIN_NAME = getattr(settings, "NOTIFY_BIN_NAME", "srk-notify")
BIN_TARGET = getattr(settings, "NOTIFY_BIN_TARGET", "/usr/local/bin")
OUTBOX = getattr(settings, "NOTIFY_OUTBOX", "/opt/srkbz-infra/notify/outbox")

if ENABLED:
    assert TARGET is not None

    apt.config.add_packages("curl")

_bin_path = join(BIN_TARGET, BIN_NAME)
_bin_template = read_file(join(dirname(__file__), "bin", "notify"))


def cleanup(dry_run: bool):
    if isdir(OUTBOX):
        assert not dry_run
        shell(f"rm -rf '{OUTBOX}'")
    if isfile(_bin_path):
        assert not dry_run
        shell(f"rm -f '{_bin_path}'")


def cleanup_needed():
    try:
        cleanup(dry_run=True)
        return False
    except:
        return True


@task()
def setup(dry_run: bool):
    if ENABLED:
        if not isdir(OUTBOX):
            assert not dry_run
            makedirs(OUTBOX, mode=0o500, exist_ok=True)

        if not isfile(_bin_path) or read_file(_bin_path) != _bin_template:
            assert not dry_run
            write_file(_bin_path, _bin_template)
            shell(f"chmod +x '{_bin_path}'")
    else:
        if isdir(OUTBOX):
            assert not dry_run
            shell(f"rm -rf '{OUTBOX}'")
        if isfile(_bin_path):
            assert not dry_run
            shell(f"rm -f '{_bin_path}'")


setup.enabled(lambda: ENABLED or cleanup_needed())
