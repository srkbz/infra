from dataclasses import dataclass
from typing import Self


@dataclass(kw_only=True, frozen=True)
class Task:
    func: callable
    requires: set[Self]
    required_by: set[Self]

    def __key(self):
        return (self.func,)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.__key() == other.__key()
        return NotImplemented
