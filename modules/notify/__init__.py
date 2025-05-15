from os.path import isdir
from os import makedirs
from framework.api import task
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


@task()
def setup(dry_run: bool):
    if not isdir(OUTBOX):
        assert not dry_run
        makedirs(OUTBOX, mode=0o500, exist_ok=True)
