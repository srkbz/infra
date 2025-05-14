import importlib
import sys
from os import getcwd, listdir
from os.path import join, dirname
from platform import node

CACHE_DIR = join(getcwd(), ".cache")
STATE_DIR = join(getcwd(), ".state")


node_settings = importlib.import_module(
    "nodes." + node().replace("-", "_") + ".settings"
)
for key in dir(node_settings):
    setattr(sys.modules[__name__], key, getattr(node_settings, key))

APT_PACKAGES = getattr(sys.modules[__name__], "APT_PACKAGES", []) + [
    "vim",
    "htop",
    "btop",
    "iftop",
    "iotop",
]
