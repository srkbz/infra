import sys
import inspect
from framework.planner import planner
from framework.task import Task


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
    return (
        task.func.__module__
        + "."
        + task.func.__qualname__
        + (" " + task.title if task.title is not None else "")
    )


class Runner:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def run(self):
        for task in planner(self.tasks):

            if inspect.isgeneratorfunction(task.func):
                gen = task.func()
                try:
                    next(gen)
                except StopIteration:
                    log.info(
                        task=task_name(task),
                        message="skipping",
                    )
                else:
                    log.warn(
                        task=task_name(task),
                        message="running",
                    )
                    for _ in gen:
                        pass
            else:
                log.warn(task=task_name(task), message="running")
                task.func()
