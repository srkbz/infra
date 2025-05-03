from dataclasses import dataclass
from typing import Self


@dataclass
class Task:
    func: callable
    requires: list[Self]
    required_by: list[Self]
