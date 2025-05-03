import sys
from framework.planner import planner
from framework.task import Task


class Logger:

    def info(self, *, task: str | None = None, message: str):
        self.line("32", task, message)

    def warn(self, *, task: str | None = None, message: str):
        self.line("33", task, message)

    def error(self, *, task: str | None = None, message: str):
        self.line("31", task, message)

    def line(self, color: str, task: str | None, message: str):
        line = ["\x1b[1;" + color + "m███ "]
        if task is not None:
            line.append("[" + task + "] ")
        line.append(message)
        line.append("\x1b[0m\n")
        sys.stdout.write("".join(line))


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
            log.info(task=task_name(task), message="running")
            task.func()
