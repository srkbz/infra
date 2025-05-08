#!/usr/bin/env bash
set -euo pipefail
SITE_HOME="$1"
rm -f "${SITE_HOME}/LIVE_COMMIT"
rm -f "${SITE_HOME}/TARGET_COMMIT"
ebrow-trigger
