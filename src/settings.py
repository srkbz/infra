from os import getcwd
from os.path import join


CACHE_DIR = join(getcwd(), ".cache")
STATE_DIR = join(getcwd(), ".state")

APT_PACKAGES = ["vim"]
