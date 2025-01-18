#!/usr/bin/env bash
set -euo pipefail

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
    restic -r "$backup_repo" check --insecure-no-password
    check_result=$?
    set -e
    if [ "$check_result" != 0 ]; then
        restic -r "$backup_repo" init --insecure-no-password
    fi

    restic -r "$backup_repo" backup --insecure-no-password "$backup_location"
done
