import sys
import inspect
from typing import Callable
from framework.models import Task
from framework.planner import planner


class Logger:

    def info(
        self,
        *,
        task: str | None = None,
        message: str,
    ):
        self.line("32", task, message)

    def warn(
        self,
        *,
        task: str | None = None,
        message: str,
    ):
        self.line("33", task, message)

    def error(
        self,
        *,
        task: str | None = None,
        message: str,
    ):
        self.line("31", task, message)

    def line(
        self,
        color: str,
        task: str | None,
        message: str,
    ):
        line = ["\x1b[1;" + color + "m███ "]
        if task is not None:
            line.append(task + " ")
        line.append(message)
        line.append("\x1b[0m\n")
        sys.stderr.write("".join(line))


log = Logger()


def task_name(task: Task):
    return (
        task.func.__module__
        + "."
        + (task.name if task.name is not None else task.func.__name__)
    )


class Runner:
    def __init__(self):
        self._tasks: list[Task] = []
        self._commands: list[tuple[str, Callable]] = []

    def add_task(self, task: Task):
        self._tasks.append(task)

    def add_command(self, name: str, func: Callable):
        self._commands.append((name, func))

    def get_tasks(self):
        return [task for task in self._tasks if task._enabled]

    def run(self):
        args = sys.argv[1:]
        if len(args) == 0:
            self.default()
        else:
            name = args[:1]
            args = args[1:]
            for command_name, command_func in self._commands:
                print(command_name)
                if command_name == name:
                    print("HEY")
                    command_func(args)

    def default(self):
        for task in self._tasks:
            task._enabled = (
                task._enabled_func()
                if task._enabled_func is not None
                else task._enabled
            )
            task._tags = (
                task._tags_func() if task._tags_func is not None else task._tags
            )

        for task in self._tasks:
            if not task._enabled:
                continue

            requires = []
            for item in task.requires:
                if callable(item):
                    requires.extend(item())
                else:
                    requires.append(item)
            task.requires.clear()
            task.requires.extend(list(dict.fromkeys(requires)))

            required_by = []
            for item in task.required_by:
                if callable(item):
                    required_by.extend(item())
                else:
                    required_by.append(item)
            task.required_by.clear()
            task.required_by.extend(list(dict.fromkeys(required_by)))

        for task in planner(self._tasks):
            func_arg_spec = inspect.getfullargspec(task.func)
            expects_dry_run_kwarg = (
                "dry_run" in func_arg_spec.annotations
                and func_arg_spec.annotations["dry_run"] == bool
            )

            skip = False

            if expects_dry_run_kwarg:
                skip = True
                try:
                    task.func(dry_run=True)
                except Exception:
                    skip = False

            if skip:
                log.info(
                    task=task_name(task),
                    message="up to date",
                )
            else:
                log.warn(task=task_name(task), message="running")
                if expects_dry_run_kwarg:
                    task.func(dry_run=False)
                else:
                    task.func()


runner = Runner()
