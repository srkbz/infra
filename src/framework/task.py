from dataclasses import dataclass
from typing import Any, Self, TypeVar

T = TypeVar("T")


@dataclass(kw_only=True, frozen=True)
class Task:
    func: callable
    requires: list[Self]
    required_by: list[Self]
    tags: list[Any]
    title: str | None

    def __key(self):
        return (self.func,)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.__key() == other.__key()
        return NotImplemented

    def get_tags(self, klazz: type[T]) -> list[T]:
        return [tag for tag in self.tags if isinstance(tag, klazz)]
