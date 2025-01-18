#!/usr/bin/env bash
set -euo pipefail

for backup_name in ./conf/*; do
    echo "- $backup_name"
done
