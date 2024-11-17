#!/usr/bin/env bash
set -euo pipefail

rm -rf ./*
chmod -R 700 .
umask 077

"${TASKFILE_DIR}/secrets-xml-to-dir.py" "$@"
