#!/usr/bin/env bash
set -euo pipefail

for file in ./conf/*; do
    backup_name="$(basename "$file")"
    backup_location="$(cat "$file")"
    echo "- $backup_name"
    echo "  $backup_location"
done
