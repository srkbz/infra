import sys
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

    def add_task(self, task: Task):
        self._tasks.append(task)

    def get_tasks(self):
        return [task for task in self._tasks if task._enabled]

    def run(self):
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

            skip = False

            if task._when_check_fails_func is not None:
                skip = True
                try:
                    task._when_check_fails_func()
                except Exception:
                    skip = False

            if skip:
                log.info(
                    task=task_name(task),
                    message="up to date",
                )
            else:
                log.warn(task=task_name(task), message="running")
                task.func()


runner = Runner()
