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
            line.append("[" + task + "] ")
        line.append(message)
        line.append("\x1b[0m\n")
        sys.stderr.write("".join(line))


log = Logger()


def task_name(task: Task):
    text: str = (
        task.func.__module__
        + "."
        + task.func.__qualname__
        + (" " + task.title if task.title is not None else "")
    )
    return text.removeprefix("modules.")


class Runner:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def run(self):
        for task in self.tasks:
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

        for task in planner(self.tasks):

            skip = False

            if len(task.when_check_fails_funcs) > 0:
                skip = True
                try:
                    for func in task.when_check_fails_funcs:
                        func()
                except Exception:
                    skip = False

            if skip:
                log.info(
                    task=task_name(task),
                    message="skipping",
                )
            else:
                log.warn(task=task_name(task), message="running")
                task.func()


runner = Runner()
