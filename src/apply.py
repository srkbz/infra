from os import getcwd
from os.path import join

from framework import runner
from framework.utils.context import context
from modules.apt import install_apt_packages, setup_apt
from modules.base_dirs import BaseDirs

CACHE_DIR = join(getcwd(), ".cache")
STATE_DIR = join(getcwd(), ".state")

APT_PACKAGES = ["vim"]

with runner():
    with context(BaseDirs(cache_dir=CACHE_DIR, state_dir=STATE_DIR)):
        install_apt_packages(APT_PACKAGES)
        setup_apt()
