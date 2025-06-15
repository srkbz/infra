from os import makedirs
from os.path import dirname

from framework.utils.shell import shell


def read_file(path, must_exist: bool = False) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        if must_exist:
            raise
        pass
    return None


def write_file(path, content, *, makeDirs: bool = True):
    if makeDirs:
        makedirs(dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def remove_all(path):
    shell(f"rm -rf '{path}'")


def ensure_perms(dry_run: bool, path: str, perm: str):
    if (
        shell(
            f"stat --format '%a' '{path}'", echo=False, captureStdout=True
        ).stdout.strip()
        != perm
    ):
        assert not dry_run
        shell(f"chmod '{perm}' '{path}'")
        return True
    return False


def ensure_owners(dry_run: bool, path: str, owners: str):
    if (
        shell(
            f"stat --format '%U:%G' '{path}'", echo=False, captureStdout=True
        ).stdout.strip()
        != owners
    ):
        assert not dry_run
        shell(f"chown '{owners}' '{path}'")
        return True
    return False


def ensure_file_content(dry_run: bool, path: str, content: str):
    if read_file(path) != content:
        assert not dry_run
        write_file(path, content)
        return True
    return False
