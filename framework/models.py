from dataclasses import dataclass
from typing import Any, Callable, Self, TypeVar

T = TypeVar("T")


@dataclass(kw_only=True)
class Task:
    func: Callable
    requires: list[Self | Callable[[], list[Self]]]
    required_by: list[Self | Callable[[], list[Self]]]
    name: str | None

    _enabled: bool
    _tags: list[Any]

    _enabled_func: Callable | None
    _tags_func: Callable | None

    def __key(self):
        return (self.func,)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.__key() == other.__key()
        return NotImplemented

    def get_tags(self, clazz: type[T]) -> list[T]:
        return [tag for tag in self._tags if isinstance(tag, clazz)]

    def tags(self, func):
        self._tags_func = func

    def enabled(self, func):
        self._enabled_func = func
