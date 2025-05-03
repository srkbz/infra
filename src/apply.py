from os import getcwd
from os.path import join

from framework import runner, task
from modules.apt import AptPackages, setup_apt
from modules.base_dirs import base_dirs

APT_PACKAGES = ["vim"]

with runner():
    with base_dirs(
        cache_dir=join(getcwd(), ".cache"), state_dir=join(getcwd(), ".state")
    ):

        @task(tags=[AptPackages(APT_PACKAGES)])
        def default():
            return
            yield

        setup_apt()
