from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class BaseDirs:
    cache_dir: str
    state_dir: str


__base_dirs = ContextVar[BaseDirs]("base_dirs", default=None)


@contextmanager
def base_dirs(*, cache_dir: str, state_dir: str):
    bd = BaseDirs(cache_dir=cache_dir, state_dir=state_dir)
    token = __base_dirs.set(bd)
    yield bd
    __base_dirs.reset(token)


def get_base_dirs() -> BaseDirs:
    return __base_dirs.get()
