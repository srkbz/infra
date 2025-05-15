import settings

ENABLED = getattr(settings, "MINIDLNA_ENABLED", False)
PORT = getattr(settings, "MINIDLNA_PORT", 8200)
DIRECTORY_ID = getattr(settings, "MINIDLNA_DIRECTORY_ID", None)
FRIENDLY_NAME = getattr(settings, "MINIDLNA_FRIENDLY_NAME", None)

if ENABLED:
    if DIRECTORY_ID is None:
        raise Exception("MINIDLNA_DIRECTORY_ID needs to be defined")

    DIRECTORY = settings.DIRECTORIES[DIRECTORY_ID]["path"]
