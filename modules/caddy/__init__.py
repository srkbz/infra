import platform
from os import makedirs
from os.path import isfile, isdir, join, dirname

from framework.api import task
from framework.utils.shell import shell
from framework.utils.fs import read_file, write_file


import settings


ENABLED = getattr(settings, "CADDY_ENABLED", False)
VERSION = getattr(settings, "CADDY_VERSION", "2.10.0")

_ARCHS = {"x86_64": "amd64", "aarch64": "arm64"}
_VARIANT = "linux_" + _ARCHS[platform.machine()]

_cache_dir = join(settings.CACHE_DIR, "caddy")
_version_dir = join(_cache_dir, "versions", VERSION)
_archive = join(_version_dir, f"caddy_{VERSION}_{_VARIANT}.deb")
_archive_url = f"https://github.com/caddyserver/caddy/releases/download/v{VERSION}/caddy_{VERSION}_{_VARIANT}.deb"

_conf_root = "/etc/caddy/Caddyfile"
_conf_root_template = join(dirname(__file__), "assets", "Caddyfile")
_conf_dir = "/etc/caddy/conf.d"


def install(dry_run: bool):
    needs_reload = False

    if not isfile(_archive):
        assert not dry_run
        makedirs(dirname(_archive), exist_ok=True)
        shell(f"curl --fail --location --output '{_archive}' '{_archive_url}'")

    if shell(
        "command -v caddy >/dev/null", check=False, echo=False
    ).exit_code != 0 or not shell(
        "caddy --version", echo=False, captureStdout=True
    ).stdout.startswith(
        f"v{VERSION} "
    ):
        assert not dry_run
        shell(f"apt-get install -y --allow-downgrades '{_archive}'")
        needs_reload = False

    if not isdir(_conf_dir):
        assert not dry_run
        makedirs(_conf_dir)

    if read_file(_conf_root) != read_file(_conf_root_template):
        assert not dry_run
        shell(f"cp '{_conf_root_template}' '{_conf_root}'")
        needs_reload = True

    if needs_reload:
        assert not dry_run
        shell("systemctl reload caddy")


@task()
def setup(dry_run: bool):
    if ENABLED:
        install(dry_run)
