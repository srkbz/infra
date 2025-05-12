from dataclasses import dataclass
import subprocess

SHELL = ["/bin/bash", "-xeuo", "pipefail", "-c"]


@dataclass(kw_only=True, frozen=True)
class ShellResult:
    exit_code: int
    stdout: str
    stderr: str


def shell(
    script,
    *,
    check: bool = True,
    captureStdout: bool = False,
    captureStderr: bool = False
):
    args = [*SHELL, script]
    stdout = subprocess.PIPE if captureStdout else None
    stderr = subprocess.PIPE if captureStderr else None
    result = subprocess.run(args, check=check, stdin=None, stdout=stdout, stderr=stderr)

    return ShellResult(
        exit_code=result.returncode,
        stdout=result.stdout.decode("utf-8") if captureStdout else None,
        stderr=result.stderr.decode("utf-8") if captureStderr else None,
    )
