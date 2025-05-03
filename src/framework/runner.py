import sys
import inspect
from framework.planner import planner
from framework.task import Task


class Logger:

    def info(
        self,
        *,
        task: str | None = None,
        tags: dict[str, str] | None = None,
        message: str,
    ):
        self.line("32", task, tags, message)

    def warn(
        self,
        *,
        task: str | None = None,
        tags: dict[str, str] | None = None,
        message: str,
    ):
        self.line("33", task, tags, message)

    def error(
        self,
        *,
        task: str | None = None,
        tags: dict[str, str] | None = None,
        message: str,
    ):
        self.line("31", task, tags, message)

    def line(
        self,
        color: str,
        task: str | None,
        tags: dict[str, str] | None,
        message: str,
    ):
        line = ["\x1b[1;" + color + "m███ "]
        if task is not None:
            line.append("[" + task + "] ")
        if tags is not None:
            line.append("[")
            for i, key in enumerate(tags):
                val = tags[key]
                line.append(f"{key}={val}")
                if i < (len(tags) - 1):
                    line.append(" ")
            line.append("] ")
        line.append(message)
        line.append("\x1b[0m\n")
        sys.stderr.write("".join(line))


log = Logger()


def task_name(task: Task):
    return task.func.__module__ + "." + task.func.__qualname__


class Runner:
    def __init__(self):
        self.__tasks: list[Task] = []

    def add_task(self, task: Task):
        self.__tasks.append(task)

    def run(self):
        for task in planner(self.__tasks):

            if inspect.isgeneratorfunction(task.func):
                gen = task.func()
                try:
                    next(gen)
                except StopIteration:
                    log.info(
                        task=task_name(task),
                        tags=task.tags,
                        message="skipping",
                    )
                else:
                    log.warn(
                        task=task_name(task),
                        tags=task.tags,
                        message="running",
                    )
                    for _ in gen:
                        pass
            else:
                log.warn(
                    task=task_name(task), tags=task.tags, message="running"
                )
                task.func()
