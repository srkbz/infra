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
_cache_dir = join(settings.CACHE_DIR, "static_sites")
_sites_state_dir = join(_state_dir, "sites")
_sites_cache_dir = join(_cache_dir, "sites")

if ENABLED:
    docker.config.enable()


def _setup(dry_run: bool):
    if not isdir(_sites_state_dir):
        assert not dry_run
        makedirs(_sites_state_dir)

    site_ids = SITES.keys()
    existing_site_ids = listdir(_sites_state_dir)

    sites_to_add = [s for s in site_ids if s not in existing_site_ids]
    sites_to_remove = [s for s in existing_site_ids if s not in site_ids]

    for site_id in sites_to_remove:
        assert not dry_run
        site_path = join(_sites_state_dir, site_id)
        shell(f"rm -rf '{site_path}'")

    for site_id in sites_to_add:
        assert not dry_run
        site_path = join(_sites_state_dir, site_id)
        makedirs(site_path)


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
    if site_id not in SITES:
        print("Unknown site: " + site_id)
        return

    build_id = uuid.uuid4().hex
    build_workspace = join(_sites_cache_dir, site_id, "builds", build_id)

    site_repository = SITES[site_id]["repository"]
    site_branch = SITES[site_id].get("branch", "master")
    site_build_script = SITES[site_id].get("build_script", None)

    print(f"Building {site_id} ({build_id})")
    makedirs(build_workspace)

    shell(
        f"git clone --depth 1 --branch '{site_branch}' '{site_repository}' '{build_workspace}'"
    )

    if site_build_script is not None:
        shell(site_build_script, cwd=build_workspace)
        # copy to live
    elif isfile(join(build_workspace, "Dockerfile")):
        shell(f"docker build -t 'static_site_{build_id}' .", cwd=build_workspace)
        container_id = shell(
            f"docker create 'static_site_{build_id}'", captureStdout=True, echo=False
        ).stdout.strip()
        # copy to live
        shell(f"docker rm -f '{container_id}'")
        shell(f"docker rmi 'static_site_{build_id}'")

    shell(f"rm -rf '{build_workspace}'")
