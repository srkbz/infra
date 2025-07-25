import uuid
import textwrap
from os import makedirs, listdir
from os.path import isfile, isdir, join

from framework.api import command, task
from framework.utils.shell import shell
from framework.utils.fs import ensure_perms

from modules import docker, caddy

import settings

SITES: dict[str, dict] = getattr(settings, "STATIC_SITES", {})

_state_dir = "/srv/srkbz/static_sites"
_cache_dir = join(settings.CACHE_DIR, "static_sites")
_sites_state_dir = join(_state_dir, "sites")
_sites_cache_dir = join(_cache_dir, "sites")


def _is_enabled():
    return len(SITES) > 0


if _is_enabled():
    docker.config.enable()
    for site_id in sorted(SITES.keys()):
        _site_state_dir = join(_sites_state_dir, site_id)
        caddy.config.add_caddyfile(
            textwrap.dedent(
                f"""
                https://{site_id} {{
                    root * {_site_state_dir}
                    encode zstd gzip

                    @versioned_urls query v=*
                    header @versioned_urls Cache-Control "public, max-age=31536000, immutable"

                    file_server
                }}
                """
            ).lstrip()
        )


def _setup(dry_run: bool):
    if not isdir(_sites_state_dir):
        assert not dry_run
        makedirs(_sites_state_dir)

    ensure_perms(dry_run, _site_state_dir, "755")

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
        _build(site_path)


def _cleanup(dry_run: bool):
    if isdir(_state_dir):
        assert not dry_run
        shell(f"rm -rf '{_state_dir}'")

    if isdir(_cache_dir):
        assert not dry_run
        shell(f"rm -rf '{_cache_dir}'")


def _needs_cleanup():
    try:
        _cleanup(dry_run=True)
        return False
    except:
        return True


def _build(site_id: str):
    build_id = uuid.uuid4().hex
    build_workspace = join(_sites_cache_dir, site_id, "builds", build_id)

    site_repository = SITES[site_id]["repository"]
    site_branch = SITES[site_id].get("branch", "master")
    site_build_script = SITES[site_id].get("build_script", None)
    site_directory = SITES[site_id].get("directory", "dist")

    site_live = join(_sites_state_dir, site_id)

    print(f"Building {site_id} ({build_id})")
    makedirs(build_workspace)

    shell(
        f"git clone --depth 1 --branch '{site_branch}' '{site_repository}' '{build_workspace}'"
    )

    if site_build_script is not None:
        site_directory_full = join(build_workspace, site_directory)
        shell(site_build_script, cwd=build_workspace)
        shell(f"rm -rf '{site_live}'")
        shell(f"cp -r '{site_directory_full}' '{site_live}'")
    elif isfile(join(build_workspace, "Dockerfile")):
        shell(f"docker build -t 'static_site_{build_id}' .", cwd=build_workspace)
        container_id = shell(
            f"docker create 'static_site_{build_id}'", captureStdout=True, echo=False
        ).stdout.strip()
        shell(f"rm -rf '{site_live}'")
        shell(f"docker cp '{container_id}:/{site_directory}' '{site_live}'")
        shell(f"docker rm -f '{container_id}'")
        shell(f"docker rmi 'static_site_{build_id}'")
    else:
        site_directory_full = join(build_workspace, site_directory)
        shell(f"rm -rf '{site_live}'")
        shell(f"cp -r '{site_directory_full}' '{site_live}'")

    shell(f"rm -rf '{build_workspace}'")


@task(requires=[docker.setup])
def setup(dry_run: bool):
    if _is_enabled():
        _setup(dry_run)
    else:
        _cleanup(dry_run)


setup.enabled(lambda: _is_enabled() or _needs_cleanup())


@command(name="static-sites-build")
def build_cmd(site_id):
    if site_id not in SITES:
        print("Unknown site: " + site_id)
        return

    _build(site_id)


@command(name="static-sites-build-all")
def build_all_cmd():
    for site_id in SITES:
        _build(site_id)
