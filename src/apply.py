from os import getcwd
from os.path import join

from framework import runner, task, get_runner, shell
from modules.apt import AptPackages, setup_apt
from modules.base_dirs import base_dirs


with runner():
    with base_dirs(
        cache_dir=join(getcwd(), ".cache"), state_dir=join(getcwd(), ".state")
    ):

        @task(tags=[AptPackages(["vim"])])
        def default():
            return
            yield

        setup_apt()
