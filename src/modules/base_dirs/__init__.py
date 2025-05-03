from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class BaseDirs:
    cache_dir: str
    state_dir: str
