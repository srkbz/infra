import platform
from os import makedirs
from os.path import isfile, isdir, join, dirname

from framework.api import task
from framework.utils.shell import shell

import settings


ENABLED = getattr(settings, "RESTIC_ENABLED", False)
VERSION = getattr(settings, "RESTIC_VERSION", "0.18.0")
BACKUPS = getattr(settings, "RESTIC_BACKUPS", {})


_ARCHS = {"x86_64": "amd64", "aarch64": "arm64"}
_VARIANT = "linux_" + _ARCHS[platform.machine()]

_cache_dir = join(settings.CACHE_DIR, "restic")
_version_dir = join(_cache_dir, "versions", VERSION)
_archive = join(_version_dir, f"restic_{VERSION}_{_VARIANT}.bz2")
_archive_verified = join(_version_dir, f"restic_{VERSION}_{_VARIANT}.bz2.verified")
_archive_url = f"https://github.com/restic/restic/releases/download/v{VERSION}/restic_{VERSION}_{_VARIANT}.bz2"
_archive_sums = join(dirname(__file__), "versions", VERSION, "SHA256SUMS")
_bin = join(_version_dir, f"restic_{VERSION}_{_VARIANT}")


def _setup(dry_run: bool):
    if not isfile(_bin):
        assert not dry_run

        if not isfile(_archive):
            makedirs(dirname(_archive), exist_ok=True)
            shell(f"curl --fail --location --output '{_archive}' '{_archive_url}'")

        if not isfile(_archive_verified):
            shell(
                f"cat '{_archive_sums}' | grep '{_VARIANT}' | sha256sum --check",
                cwd=dirname(_archive),
            )
            shell(f"touch '{_archive_verified}'")

        shell(
            f"bzip2 -d 'restic_{VERSION}_{_VARIANT}.bz2'",
            cwd=dirname(_archive),
        )
        shell(f"chmod +x '{_bin}'")


def _cleanup(dry_run: bool):
    if isdir(_cache_dir):
        assert not dry_run
        shell(f"rm -rf '{_cache_dir}'")


def cleanup_needed():
    try:
        _cleanup(dry_run=True)
        return False
    except:
        return True


@task()
def setup(dry_run: bool):
    if ENABLED:
        _setup(dry_run)
    else:
        _cleanup(dry_run)


setup.enabled(lambda: ENABLED or cleanup_needed())
