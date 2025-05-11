from framework.api import task
from modules.apt import AptPackages

import settings

ENABLED = getattr(settings, "MINIDLNA_ENABLED", False)


@task(enabled=ENABLED, tags=[AptPackages(["minidlna"])])
def setup():
    print("Minidlna!")
