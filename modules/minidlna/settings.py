import settings

PORT = getattr(settings, "MINIDLNA_PORT", 8200)
DIRECTORY_ID = getattr(settings, "MINIDLNA_DIRECTORY_ID", None)
FRIENDLY_NAME = getattr(settings, "MINIDLNA_FRIENDLY_NAME", None)


def is_enabled():
    return DIRECTORY_ID is not None


if is_enabled():
    DIRECTORY = settings.DIRECTORIES[DIRECTORY_ID]["path"]
