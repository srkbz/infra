from .settings import *


def build_conf():
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
