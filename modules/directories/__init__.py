from dataclasses import dataclass

from framework.api import task
from framework.utils.shell import shell
from framework.runner import runner

import settings

DIRECTORIES = getattr(settings, "DIRECTORIES", [])


@dataclass(frozen=True)
class Directory:
    directory_id: str


def get_tasks_with_directories(directory_id: str):
    def _():
        return [
            task
            for task in runner.get_tasks()
            if any([t.directory_id == directory_id for t in task.get_tags(Directory)])
        ]

    return _


setup = {}


def define_setup(directory_id: str):

    directory = DIRECTORIES[directory_id]
    directory_path = directory["path"]
    directory_perm = directory["perm"]
    directory_owner = ":".join(directory["owner"])

    @task(required_by=[get_tasks_with_directories(directory_id)])
    def _setup():
        shell(f"mkdir -p '{directory_path}'")
        shell(f"chmod '{directory_perm}' '{directory_path}'")
        shell(f"chown '{directory_owner}' '{directory_path}'")

    _setup.func.__name__ = f"setup[{directory_id}]"
    setup[directory_id] = _setup

    @_setup.when_check_fails
    def _():
        shell(f"test -d '{directory_path}'", echo=False)
        shell(
            f"[ \"$(stat --format '%a' '{directory_path}')\" == '{directory_perm}' ]",
            echo=False,
        )
        shell(
            f"[ \"$(stat --format '%U:%G' '{directory_path}')\" == '{directory_owner}' ]",
            echo=False,
        )


for directory_id in DIRECTORIES:
    define_setup(directory_id)
