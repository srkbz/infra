import platform
from os import makedirs
from os.path import isfile, join, dirname

from framework.api import task
from framework.utils.shell import shell

import settings


ENABLED = getattr(settings, "RESTIC_ENABLED", False)
VERSION = getattr(settings, "RESTIC_VERSION", "0.18.0")
BACKUPS = getattr(settings, "RESTIC_BACKUPS", {})


_VARIANTS = {"x86_64": "amd64", "aarch64": "arm64"}
_VARIANT = _VARIANTS[platform.machine()]

_CACHE_DIR = settings.CACHE_DIR

_version_dir = join(_CACHE_DIR, "restic", "versions", VERSION)
_archive = join(_version_dir, "archive.bz2")
_archive_verified = join(_version_dir, "archive.verified")
_archive_url = f"https://github.com/restic/restic/releases/download/v{VERSION}/restic_{VERSION}_linux_{_VARIANT}.bz2"
_archive_sums = join(dirname(__file__), "versions", VERSION, "SHA256SUMS")
_bin = join(_version_dir, f"restic_{VERSION}_{_VARIANT}")


@task()
def install(dry_run: bool):
    if not isfile(_archive):
        assert not dry_run
        makedirs(dirname(_archive), exist_ok=True)
        shell(f"curl --fail --location --output '{_archive}' '{_archive_url}'")
    if not isfile(_archive_verified):
        assert not dry_run
        shell(f"cat '{_archive_sums}' | grep '{_VARIANT}' | sha256sum --check")
        shell(f"touch '{_archive_verified}'")
    if not isfile(_bin):
        assert not dry_run
        shell(
            f"bzip2 -d 'restic_{VERSION}_{_VARIANT}.bz2'",
            cwd=dirname(_archive),
        )
        shell(f"chmod +x '{_bin}'")


install.enabled(lambda: ENABLED)
