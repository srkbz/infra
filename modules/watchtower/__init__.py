from os.path import join, isfile, isdir, dirname
from os import makedirs

from framework.api import task
from framework.utils.shell import shell
from framework.utils.fs import read_file, remove_all

from modules import docker

import settings

ENABLED = getattr(settings, "WATCHTOWER_ENABLED", False)

_base_compose_file = join(dirname(__file__), "docker-compose.yml")

_state_dir = join(settings.STATE_DIR, "watchtower")
_compose_file = join(_state_dir, "docker-compose.yml")


if ENABLED:
    docker.config.enable()


def up(dry_run: bool):
    if not isdir(_state_dir):
        assert not dry_run
        makedirs(_state_dir)

    if not isfile(_compose_file) or read_file(_base_compose_file) != read_file(
        _compose_file
    ):
        assert not dry_run
        shell(f"cp '{_base_compose_file}' '{_compose_file}'")

    if (
        shell(
            "docker compose ps -q", cwd=_state_dir, captureStdout=True, echo=False
        ).stdout.strip()
        == ""
    ):
        assert not dry_run
        shell("docker compose up -d", cwd=_state_dir)


def down(dry_run: bool):
    if isfile(_compose_file):
        assert not dry_run
        shell("docker compose down --volumes --remove-orphans", cwd=_state_dir)

    if isdir(_state_dir):
        assert not dry_run
        remove_all(_state_dir)


def cleanup_needed():
    try:
        down(dry_run=True)
        return False
    except:
        return True


@task(requires=[docker.setup])
def setup(dry_run: bool):
    up(dry_run)


setup.enabled(lambda: ENABLED or cleanup_needed())
