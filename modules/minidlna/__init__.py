from framework.api import task
from framework.utils.fs import read_file, write_file
from framework.utils.shell import shell

from modules.apt import AptPackages

from modules.directories import Directory
import settings

ENABLED = getattr(settings, "MINIDLNA_ENABLED", False)
PORT = getattr(settings, "MINIDLNA_PORT", 8200)
DIRECTORY_ID = getattr(settings, "MINIDLNA_DIRECTORY_ID", None)
FRIENDLY_NAME = getattr(settings, "MINIDLNA_FRIENDLY_NAME", None)

if ENABLED:
    if DIRECTORY_ID is None:
        raise Exception("MINIDLNA_DIRECTORY_ID needs to be defined")

    DIRECTORY = settings.DIRECTORIES[DIRECTORY_ID]["path"]


def build_config():
    return "\n".join(
        [
            "# man minidlna.conf",
            "",
            "media_dir=" + DIRECTORY,
            "port=" + str(PORT),
            "inotify=yes",
            "root_container=B",
            *(["friendly_name=" + FRIENDLY_NAME] if FRIENDLY_NAME is not None else []),
            "album_art_names=Cover.jpg/cover.jpg/AlbumArtSmall.jpg/albumartsmall.jpg",
            "album_art_names=AlbumArt.jpg/albumart.jpg/Album.jpg/album.jpg",
            "album_art_names=Folder.jpg/folder.jpg/Thumb.jpg/thumb.jpg",
            "",
        ]
    )


@task()
def setup():
    write_file("/etc/minidlna.conf", build_config())
    shell("systemctl restart minidlna.service")


@setup.enabled
def _():
    return ENABLED


@setup.tags
def _():
    return [AptPackages(["minidlna"]), Directory(DIRECTORY_ID)]


@setup.when_check_fails
def _():
    assert read_file("/etc/minidlna.conf") == build_config()
    shell("systemctl status minidlna.service >/dev/null", echo=False)
