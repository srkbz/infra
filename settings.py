from os import getcwd
from os.path import join
from platform import node

CACHE_DIR = join(getcwd(), ".cache")
STATE_DIR = join(getcwd(), ".state")

match node():
    case "srk-laptop":
        from nodes.srk_laptop.settings import *
