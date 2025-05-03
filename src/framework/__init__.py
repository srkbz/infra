from contextvars import ContextVar
from contextlib import contextmanager

from framework.tags import task_tag, TaskTagData


class Runner:
    def __init__(self):
        self.__tasks = []

    def add_task(self, func):
        self.__tasks.append(func)

    def run(self):
        for task in self.__tasks:
            task()


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
        task_tag.tag(func, TaskTagData(requires=requires, required_by=required_by))
        __runner.get().add_task(func)
        return func

    return decorator
