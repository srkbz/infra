from os import makedirs
from os.path import isfile, join, dirname
from framework.utils.shell import shell

import settings

MOONLIGHT_VERSION = getattr(settings, "TV_MOONLIGHT_VERSION", "6.1.0")
_moonlight_url = f"https://github.com/moonlight-stream/moonlight-qt/releases/download/v{MOONLIGHT_VERSION}/Moonlight-{MOONLIGHT_VERSION}-x86_64.AppImage"
_moonlight_root = f"/opt/srkbz/tv/moonlight/{MOONLIGHT_VERSION}"
_moonlight_bin = join(_moonlight_root, "moonlight.AppImage")
_moonlight_bin_public = "/usr/local/bin/moonlight"


def setup_moonlight(dry_run: bool):
    if not isfile(_moonlight_bin):
        assert not dry_run
        makedirs(_moonlight_root, exist_ok=True)
        shell(f"curl -Lo '{_moonlight_bin}' '{_moonlight_url}'")
        shell(f"chmod +x '{_moonlight_bin}'")

    if (
        shell(
            f"readlink -f '{_moonlight_bin_public}'", check=False, captureStdout=True
        ).stdout
        != _moonlight_bin
    ):
        assert not dry_run
        shell(f"ln -fs '{_moonlight_bin}' '{_moonlight_bin_public}'")
