import json
import uuid
from os import makedirs, listdir
from os.path import isfile, isdir, join, dirname

from framework.api import command, task
from framework.utils.shell import shell
from framework.utils.fs import read_file, write_file

from modules import docker

import settings

ENABLED = getattr(settings, "STATIC_SITES_ENABLED", False)
SITES: dict[str, dict] = getattr(settings, "STATIC_SITES", {})

_state_dir = join(settings.STATE_DIR, "static_sites")
_sites_dir = join(_state_dir, "sites")

if ENABLED:
    docker.config.enable()


def _setup(dry_run: bool):
    if not isdir(_sites_dir):
        assert not dry_run
        makedirs(_sites_dir)

    site_ids = SITES.keys()
    existing_site_ids = listdir(_sites_dir)

    sites_to_add = [s for s in site_ids if s not in existing_site_ids]
    sites_to_remove = [s for s in existing_site_ids if s not in site_ids]

    for site_id in sites_to_remove:
        assert not dry_run
        site_path = join(_sites_dir, site_id)
        shell(f"rm -rf '{site_path}'")

    for site_id in sites_to_add:
        assert not dry_run
        site_path = join(_sites_dir, site_id)
        makedirs(site_path)

    for site_id, site_config in SITES.items():
        site_path = join(_sites_dir, site_id)
        site_config_path = join(site_path, "CONFIG")
        site_config_json = json.dumps(site_config, indent=2) + "\n"
        if read_file(site_config_path) != site_config_json:
            assert not dry_run
            write_file(site_config_path, site_config_json)


def _cleanup(dry_run: bool):
    if not isdir(_state_dir):
        assert not dry_run
        shell(f"rm -rf '{_state_dir}'")


def _needs_cleanup():
    try:
        _cleanup(dry_run=True)
        return False
    except:
        return True


@task(requires=[docker.setup])
def setup(dry_run: bool):
    if ENABLED:
        _setup(dry_run)
    else:
        _cleanup(dry_run)


setup.enabled(lambda: ENABLED or _needs_cleanup())


@command(name="static-sites-build")
def build_cmd(site_id):
    _build_id = uuid.uuid4().hex
    print(f"Building {site_id} ({_build_id})")
