from framework.api import task
from framework.utils.fs import read_file, write_file
from framework.utils.shell import shell

from modules.apt import AptPackages

import settings

ENABLED = getattr(settings, "MINIDLNA_ENABLED", False)
PORT = getattr(settings, "MINIDLNA_PORT", 8200)
DIRECTORY = getattr(settings, "MINIDLNA_DIRECTORY")


def build_config():
    return "\n".join(
        [
            "# man minidlna.conf",
            "",
            "media_dir=" + DIRECTORY,
            "port=" + str(PORT),
            "inotify=yes",
            "album_art_names=Cover.jpg/cover.jpg/AlbumArtSmall.jpg/albumartsmall.jpg",
            "album_art_names=AlbumArt.jpg/albumart.jpg/Album.jpg/album.jpg",
            "album_art_names=Folder.jpg/folder.jpg/Thumb.jpg/thumb.jpg",
            "",
        ]
    )


@task(enabled=ENABLED, tags=[AptPackages(["minidlna"])])
def setup():
    write_file("/etc/minidlna.conf", build_config())
    shell("systemctl restart minidlna.service")


@setup.when_check_fails
def _():
    assert read_file("/etc/minidlna.conf") == build_config()
    shell("systemctl status minidlna.service")
