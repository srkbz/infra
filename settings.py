from os import getcwd
from os.path import join
from platform import node

CACHE_DIR = join(getcwd(), ".cache")
STATE_DIR = join(getcwd(), ".state")
APT_PACKAGES = ["vim", "htop", "btop", "iftop", "iotop"]

match node():
    case "pi":
        from nodes.pi.settings import *
