#!/usr/bin/env bash
set -euo pipefail

rm -f "/srv/srkbz/static-sites/${1}/TARGET_COMMIT"
touch /srv/srkbz/triggers/APPLY
