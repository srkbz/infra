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

    @task(
        name=f"setup[{directory_id}]",
        required_by=[get_tasks_with_directories(directory_id)],
    )
    def _setup(dry_run: bool):
        if dry_run:
            shell(f"test -d '{directory_path}'", echo=False)
            shell(
                f"[ \"$(stat --format '%a' '{directory_path}')\" == '{directory_perm}' ]",
                echo=False,
            )
            shell(
                f"[ \"$(stat --format '%U:%G' '{directory_path}')\" == '{directory_owner}' ]",
                echo=False,
            )
            return

        shell(f"mkdir -p '{directory_path}'")
        shell(f"chmod '{directory_perm}' '{directory_path}'")
        shell(f"chown '{directory_owner}' '{directory_path}'")

    setup[directory_id] = _setup


for directory_id in DIRECTORIES:
    define_setup(directory_id)
