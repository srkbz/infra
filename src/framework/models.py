from dataclasses import dataclass
from typing import Any, Callable, Self, TypeVar

T = TypeVar("T")


@dataclass(kw_only=True, frozen=True)
class Task:
    func: callable
    enabled: bool
    requires: list[Self | Callable[[], list[Self]]]
    required_by: list[Self | Callable[[], list[Self]]]
    tags: list[Any]
    title: str | None
    when_check_fails_funcs: list[Callable]

    def __key(self):
        return (self.func,)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.__key() == other.__key()
        return NotImplemented

    def get_tags(self, clazz: type[T]) -> list[T]:
        return [tag for tag in self.tags if isinstance(tag, clazz)]

    def when_check_fails(self, func):
        self.when_check_fails_funcs.append(func)
