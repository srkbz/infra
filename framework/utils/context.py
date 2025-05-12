from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any, TypeVar


@dataclass(kw_only=True, frozen=True)
class ContextData:
    values: dict[type, Any]


__context = ContextVar[ContextData | None]("context", default=None)


@contextmanager
def context(*values: Any):
    parent_context_data = __context.get()

    context_data = ContextData(
        values={
            **(parent_context_data.values if parent_context_data is not None else {})
        }
    )
    for value in values:
        context_data.values[value.__class__] = value

    token = __context.set(context_data)
    yield
    __context.reset(token)


T = TypeVar("T")


def get_context_value(klazz: type[T]) -> T | None:
    context_data = __context.get()
    if context_data is None:
        return None
    return context_data.values.get(klazz)
