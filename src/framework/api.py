import inspect
from typing import Any, Callable

from framework.models import Task
from framework.runner import runner


def task(
    *,
    requires: list[Task | Callable[[], list[Task]]] = [],
    required_by: list[Task | Callable[[], list[Task]]] = [],
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
            when_check_fails_funcs=[],
        )
        runner.add_task(task)

        if inspect.ismethod(func):
            setattr(func.__self__, func.__name__, task)

        return task

    return decorator
