#!/usr/bin/env bash
set -euo pipefail

rm -rf ./*
chmod -R 700 .
umask 077

"${WD}/secrets-xml-to-dir.py" "$@"
