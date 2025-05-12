from os import makedirs
from os.path import dirname

from framework.utils.shell import shell


def read_file(path) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        pass
    return None


def write_file(path, content, *, makeDirs: bool = True):
    if makeDirs:
        makedirs(dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def remove_all(path):
    shell(f"rm -rf '{path}'")
