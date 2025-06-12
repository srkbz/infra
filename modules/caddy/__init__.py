import platform
from os import makedirs
from os.path import isfile, isdir, join, dirname

from framework.api import task
from framework.utils.shell import shell
from framework.utils.fs import read_file, write_file


import settings


class Config:
    def __init__(self):
        self._caddyfiles: list[str] = []

    def add_caddyfile(self, caddyfile):
        self._caddyfiles.append(caddyfile)


config = Config()


ENABLED = getattr(settings, "CADDY_ENABLED", False)
VERSION = getattr(settings, "CADDY_VERSION", "2.10.0")
CADDYFILES = getattr(settings, "CADDY_CADDYFILES", [])

_ARCHS = {"x86_64": "amd64", "aarch64": "arm64"}
_VARIANT = "linux_" + _ARCHS[platform.machine()]

_cache_dir = join(settings.CACHE_DIR, "caddy")
_version_dir = join(_cache_dir, "versions", VERSION)
_archive = join(_version_dir, f"caddy_{VERSION}_{_VARIANT}.deb")
_archive_url = f"https://github.com/caddyserver/caddy/releases/download/v{VERSION}/caddy_{VERSION}_{_VARIANT}.deb"

_conf_root = "/etc/caddy/Caddyfile"
_conf_root_template = join(dirname(__file__), "assets", "Caddyfile")
_conf_dir = "/etc/caddy/conf.d"
_conf_count = join(_conf_dir, "COUNT")


def _setup(dry_run: bool):
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

    if not isdir(_conf_dir):
        assert not dry_run
        makedirs(_conf_dir)

    if str(len(config._caddyfiles)) != read_file(_conf_count):
        assert not dry_run
        shell(f"rm -rf '{_conf_dir}'/*")
        write_file(_conf_count, str(len(config._caddyfiles)))
        needs_reload = True

    for i, caddyfile in enumerate(CADDYFILES + config._caddyfiles):
        if read_file(join(_conf_dir, f"{str(i)}.conf")) != caddyfile:
            assert not dry_run
            write_file(join(_conf_dir, f"{str(i)}.conf"), caddyfile)
            needs_reload = True

    if read_file(_conf_root) != read_file(_conf_root_template):
        assert not dry_run
        shell(f"cp '{_conf_root_template}' '{_conf_root}'")
        needs_reload = True

    if needs_reload:
        assert not dry_run
        shell("systemctl reload caddy")


def _cleanup(dry_run: bool):
    if shell("command -v caddy >/dev/null", check=False, echo=False).exit_code == 0:
        assert not dry_run
        shell(f"apt-get remove -y caddy")

    if isfile(_conf_root):
        assert not dry_run
        shell(f"rm -f '{_conf_root}'")

    if isdir(_conf_dir):
        assert not dry_run
        shell(f"rm -rf '{_conf_dir}'")

    if isdir(_cache_dir):
        assert not dry_run
        shell(f"rm -rf '{_cache_dir}'")


def _cleanup_needed():
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


setup.enabled(lambda: ENABLED or _cleanup_needed())
