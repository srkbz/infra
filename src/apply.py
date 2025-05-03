from os import getcwd
from os.path import join

from framework import runner
from modules.apt import install_apt_packages, setup_apt
from modules.base_dirs import base_dirs

CACHE_DIR = join(getcwd(), ".cache")
STATE_DIR = join(getcwd(), ".state")

APT_PACKAGES = ["vim"]

with runner():
    with base_dirs(cache_dir=CACHE_DIR, state_dir=STATE_DIR):

        install_apt_packages(APT_PACKAGES)

        setup_apt()
