from contextvars import ContextVar
from contextlib import contextmanager

from framework.runner import Runner
from framework.task import Task


__runner = ContextVar[Runner]("runner", default=None)


@contextmanager
def runner():
    r = Runner()
    token = __runner.set(r)
    yield r
    r.run()
    __runner.reset(token)


def task(requires: set[callable] = set(), required_by: set[callable] = set()):
    def decorator(func):
        task = Task(func=func, requires=requires, required_by=required_by)
        __runner.get().add_task(task)
        return task

    return decorator
