# Sway
# mod key is Home
# 1920x1080 60hz
# menu opens on Home + OK
# blueman-manager
# pavucontrol
# moonlight
# navigate workspace on Home + Number
# switch between windows with Home + directional pad
# close current window with Home + Q
# shutdown/restart menu with Home + Esc
# auto-login and launch sway on boot
from os.path import isfile
from os import makedirs
import textwrap

from framework.api import task
from framework.utils.fs import read_file, write_file
from framework.utils.shell import shell

from modules import apt

import settings

ENABLED = getattr(settings, "TV_ENABLED", False)
USER = getattr(settings, "TV_USER", "tv")

if ENABLED:
    apt.config.add_packages("sway", "pavucontrol", "blueman")


def _setup(dry_run: bool):
    if (
        shell(f"getent passwd '{USER}' >/dev/null", check=False, echo=False).exit_code
        != 0
    ):
        assert not dry_run
        shell(f"useradd --create-home --shell /bin/bash '{USER}'")

    if "# srkbz infra - sway on tty" not in read_file("/home/tv/.bashrc"):
        assert not dry_run
        write_file(
            "/home/tv/.bashrc",
            read_file("/home/tv/.bashrc")
            + "\n\n"
            + textwrap.dedent(
                f"""
                # srkbz infra - sway on tty
                if [ -z "$WAYLAND_DISPLAY" ] && [ -n "$XDG_VTNR" ] && [ "$XDG_VTNR" -eq 1 ] ; then
                    exec sway
                fi
                """
            ).lstrip(),
        )

    autologin_conf = textwrap.dedent(
        f"""
        [Service]
        Type=simple
        Environment=XDG_SESSION_TYPE=wayland
        ExecStart=
        ExecStart=-/sbin/agetty -o '-p -f -- \\u' --noclear --autologin '{USER}' %I /bin/bash
        """
    ).lstrip()

    if (
        read_file("/etc/systemd/system/getty@tty1.service.d/autologin.conf")
        != autologin_conf
    ):
        assert not dry_run
        makedirs("/etc/systemd/system/getty@tty1.service.d", exist_ok=True)
        write_file(
            "/etc/systemd/system/getty@tty1.service.d/autologin.conf", autologin_conf
        )


def _cleanup(dry_run: bool):
    pass


def _needs_cleanup():
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


setup.enabled(lambda: ENABLED or _needs_cleanup())
