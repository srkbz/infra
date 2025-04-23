#!/usr/bin/env python3
import subprocess
import sys
import os


def main():
    lines = [
        "Package: " + os.environ.get("METAPKG_NAME"),
        "Version: 0.0.0",
        "Architecture: all",
        "Description: Metapackage containing all the packages needed",
        "Depends: " + ", ".join(packages()),
    ]
    print("\n".join(lines))


def packages() -> list[str]:
    cmd = subprocess.run(
        [
            os.environ.get("EBRO_BIN"),
            "-i",
            "--query",
            'tasks | filter("apt.packages" in .labels) | map(.labels["apt.packages"]) | join("\n")',
        ],
        cwd=os.environ.get("EBRO_ROOT"),
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    output: str = cmd.stdout.encode("utf-8")
    return output.splitlines()


main()
