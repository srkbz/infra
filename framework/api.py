import inspect
from typing import Any, Callable

from framework.models import Task
from framework.runner import runner


def task(
    *,
    requires: list[Task | Callable[[], list[Task]]] = [],
    required_by: list[Task | Callable[[], list[Task]]] = [],
    name: str | None = None,
):
    def decorator(func) -> Task:
        task = Task(
            func=func,
            requires=requires,
            required_by=required_by,
            name=name,
            _enabled=True,
            _tags=[],
            _enabled_func=None,
            _tags_func=None,
        )
        runner.add_task(task)

        if inspect.ismethod(func):
            setattr(func.__self__, func.__name__, task)

        return task

    return decorator


def command(*, name: str):
    def decorator(func):
        runner.add_command(name, func)
        return func

    return decorator
