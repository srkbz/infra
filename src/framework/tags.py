from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar

T = TypeVar("T")


class BaseTag(Generic[T]):
    def __init__(self, attribute: str):
        self._attribute = attribute

    def tag(self, obj: Any, data: T) -> None:
        setattr(obj, self._attribute, data)

    def read(self, obj: Any) -> Optional[T]:
        return getattr(obj, self._attribute, None)


@dataclass
class TaskTagData:
    requires: list[callable]
    required_by: list[callable]


task_tag = BaseTag[TaskTagData]("_framework_task")
