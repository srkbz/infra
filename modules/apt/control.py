#!/usr/bin/env python3
import subprocess
import sys
import os


def main():
    packages = get_packages()
    print("### Packages to install: " + str(len(packages)), file=sys.stderr)
    for package in packages:
        print("### - " + package, file=sys.stderr)

    lines = [
        "Package: " + os.environ.get("METAPKG_NAME"),
        "Version: 0.0.0",
        "Architecture: all",
        "Description: Metapackage containing all the packages needed",
        *(["Depends: " + ", ".join(packages)] if len(packages) > 0 else []),
    ]

    print("\n".join(lines))


def get_packages() -> list[str]:
    cmd = subprocess.run(
        [
            os.environ.get("EBRO_BIN"),
            "-i",
            "--query",
            'tasks | filter("apt.packages" in .labels) | map(.labels["apt.packages"]) | join("\\n")',
        ],
        cwd=os.environ.get("EBRO_ROOT"),
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    output: str = cmd.stdout.decode("utf-8")
    return list(dict.fromkeys(output.splitlines()))


main()
