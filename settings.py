import importlib
import sys
from os import getcwd, listdir
from os.path import join, dirname
from platform import node

CACHE_DIR = join(getcwd(), ".cache")
STATE_DIR = join(getcwd(), ".state")
APT_PACKAGES = ["vim", "htop", "btop", "iftop", "iotop"]


node_settings = importlib.import_module("nodes." + node() + ".settings")
for key in node_settings:
    setattr(sys.modules[__name__], key, node_settings[key])
