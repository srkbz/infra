from os import listdir
from os.path import isdir, join

from framework.api import task
from framework.utils.shell import shell
from framework.utils.fs import (
    ensure_file_content,
    ensure_owners,
    ensure_perms,
)

from modules import apt


class Config:
    def __init__(self):
        self._interfaces: list[str] = []

    def add_interface(self, interface):
        if len(self._interfaces) == 0:
            apt.config.add_packages("wireguard")
        self._interfaces.append(interface)


config = Config()


_wireguard_conf_home = "/etc/wireguard"


def _setup(dry_run: bool):
    for i, interface in enumerate(config._interfaces):
        conf_name = f"wg{str(i)}"
        conf_file = join(_wireguard_conf_home, f"{conf_name}.conf")
        if any(
            [
                ensure_file_content(dry_run, conf_file, interface),
                ensure_perms(dry_run, conf_file, "600"),
                ensure_owners(dry_run, conf_file, "root:root"),
                shell(
                    f"systemctl status 'wg-quick@{conf_name}'>/dev/null",
                    echo=False,
                    check=False,
                ).exit_code
                != 0,
            ]
        ):
            assert not dry_run
            shell(f"systemctl enable 'wg-quick@{conf_name}'")
            shell(f"systemctl start 'wg-quick@{conf_name}'")
            shell(f"wg syncconf '{conf_name}' <(wg-quick strip '{conf_name}')")


def _cleanup(dry_run: bool):
    for interface_name in [
        n.removesuffix(".conf") for n in listdir(_wireguard_conf_home)
    ]:
        shell(f"systemctl stop 'wg-quick@{interface_name}'")

    if not isdir(_wireguard_conf_home):
        return

    if len(listdir(_wireguard_conf_home)) != 0:
        assert not dry_run
        shell(f"rm -rf '{_wireguard_conf_home}'/*")


def _needs_cleanup():
    try:
        _cleanup(dry_run=True)
        return False
    except:
        return True


def _is_enabled():
    return len(config._interfaces) > 0


@task(
    requires=[apt.install_packages] if _is_enabled() else [],
    required_by=(
        [apt.install_packages] if not _is_enabled() and _needs_cleanup() else []
    ),
)
def setup(dry_run: bool):
    if _is_enabled():
        _setup(dry_run)
    else:
        _cleanup(dry_run)


setup.enabled(lambda: _is_enabled() or _needs_cleanup())
