#!/usr/bin/env bash
set -euo pipefail

rm -rf ./*
chmod -R 700 .
umask 077

"${EBRO_TASK_WORKING_DIRECTORY}/secrets-xml-to-dir.py" "$@"
