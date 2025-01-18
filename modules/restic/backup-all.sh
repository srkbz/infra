#!/usr/bin/env bash
set -euo pipefail

for file in ./conf/*; do
    backup_name="$(basename "$file")"
    echo "- $backup_name"
done
