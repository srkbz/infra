import inspect
from contextvars import ContextVar
from contextlib import contextmanager
from typing import Any

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


def get_runner():
    return __runner.get()


def task(
    *,
    requires: list[callable] = [],
    required_by: list[callable] = [],
    tags: list[Any] = [],
    title: str | None = None,
):
    def decorator(func) -> Task:
        task = Task(
            func=func,
            requires=requires,
            required_by=required_by,
            title=title,
            tags=tags,
        )
        get_runner().add_task(task)

        if inspect.ismethod(func):
            setattr(func.__self__, func.__name__, task)

        return task

    return decorator
