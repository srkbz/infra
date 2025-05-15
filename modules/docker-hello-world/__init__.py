from framework.api import task
from framework.utils.shell import shell

from modules import docker

import settings

ENABLED = getattr(settings, "DOCKER_HELLO_WORLD_ENABLED", False)

if ENABLED:
    docker.config.enable()


@task(requires=[docker.setup])
def run():
    shell("docker run --rm hello-world")


run.enabled(lambda: ENABLED)
