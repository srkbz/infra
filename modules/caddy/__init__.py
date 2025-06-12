import platform
from os import makedirs
from os.path import isfile, isdir, join, dirname

from framework.api import task
from framework.utils.shell import shell


import settings


ENABLED = getattr(settings, "CADDY_ENABLED", False)
VERSION = getattr(settings, "CADDY_VERSION", "2.10.0")

_ARCHS = {"x86_64": "amd64", "aarch64": "arm64"}
_VARIANT = "linux_" + _ARCHS[platform.machine()]

_cache_dir = join(settings.CACHE_DIR, "caddy")
_version_dir = join(_cache_dir, "versions", VERSION)
_archive = join(_version_dir, f"caddy_{VERSION}_{_VARIANT}.deb")
_archive_verified = _archive + ".verified"
_archive_url = f"https://github.com/caddyserver/caddy/releases/download/v{VERSION}/caddy_{VERSION}_{_VARIANT}.deb"
_archive_sums = join(
    dirname(__file__), "versions", VERSION, f"caddy_{VERSION}_checksums.txt"
)


def install(dry_run: bool):
    if not isfile(_archive):
        assert not dry_run
        makedirs(dirname(_archive), exist_ok=True)
        shell(f"curl --fail --location --output '{_archive}' '{_archive_url}'")

    if not isfile(_archive_verified):
        shell(
            f"cat '{_archive_sums}' | grep '{_VARIANT}' | sha256sum --check",
            cwd=dirname(_archive),
        )
        shell(f"touch '{_archive_verified}'")

    if shell(
        "command -v caddy >/dev/null", check=False, echo=False
    ).exit_code != 0 or not shell(
        "caddy --version", echo=False, captureStdout=True
    ).stdout.startswith(
        f"v{VERSION} "
    ):
        assert not dry_run
        shell(f"apt-get install -y --allow-downgrades '{_archive}'")


@task()
def setup(dry_run: bool):
    if ENABLED:
        install(dry_run)
