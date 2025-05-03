from contextvars import ContextVar
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Self


@dataclass
class Task:
    func: callable
    requires: list[Self]
    required_by: list[Self]


class Runner:
    def __init__(self):
        self.__tasks: list[Task] = []

    def add_task(self, task: Task):
        self.__tasks.append(task)

    def run(self):
        for task in self.__tasks:
            task.func()


__runner = ContextVar[Runner]("runner", default=None)


@contextmanager
def runner():
    r = Runner()
    token = __runner.set(r)
    yield r
    r.run()
    __runner.reset(token)


def task(requires: list[callable] = [], required_by: list[callable] = []):
    def decorator(func):
        task = Task(func=func, requires=requires, required_by=required_by)
        __runner.get().add_task(task)
        return task

    return decorator
