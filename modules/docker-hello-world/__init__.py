from framework.api import task
from framework.utils.shell import shell


@task()
def run():
    shell("docker run --rm hello-world")
