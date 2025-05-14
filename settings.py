import importlib
import sys
from os import getcwd
from os.path import join
from platform import node

node_settings = importlib.import_module(
    "nodes." + node().replace("-", "_") + ".settings"
)
for key in dir(node_settings):
    setattr(sys.modules[__name__], key, getattr(node_settings, key))

CACHE_DIR = getattr(sys.modules[__name__], "CACHE_DIR", join(getcwd(), ".cache"))
STATE_DIR = getattr(sys.modules[__name__], "STATE_DIR", join(getcwd(), ".state"))

APT_PACKAGES = getattr(sys.modules[__name__], "APT_PACKAGES", []) + [
    "vim",
    "htop",
    "btop",
    "iftop",
    "iotop",
]
