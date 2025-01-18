#!/usr/bin/env bash
set -euo pipefail

SECRETS_FILE="$1"

. "$SECRETS_FILE"

for file in ./conf/*; do
    backup_name="$(basename "$file")"
    backup_location="$(cat "$file")"
    backup_repo="${BASE_URL}/${BUCKET_NAME}/${backup_name}"
    export AWS_ACCESS_KEY_ID="$KEY_ID"
    export AWS_SECRET_ACCESS_KEY="$APP_KEY"
    echo "- $backup_name"
    echo "  $backup_location"

    set -x

    set +e
    ./bin/restic -r "$backup_repo" snapshots --insecure-no-password >/dev/null
    check_result=$?
    set -e
    if [ "$check_result" != 0 ]; then
        ./bin/restic -r "$backup_repo" init --insecure-no-password
    fi

    ./bin/restic -r "$backup_repo" backup \
        --skip-if-unchanged \
        --insecure-no-password \
        "$backup_location"
done
