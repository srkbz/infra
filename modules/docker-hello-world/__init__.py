from framework.api import task
from framework.utils.shell import shell

from modules.docker import config as docker_config, setup

docker_config.enable()


@task(requires=[setup])
def run():
    shell("docker run --rm hello-world")
