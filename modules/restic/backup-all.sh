#!/usr/bin/env bash
set -euo pipefail

for backup_name in "${RESTIC_HOME}/conf"/*; do
    echo "- $backup_name"
done
