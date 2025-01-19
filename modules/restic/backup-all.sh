#!/usr/bin/env bash
set -euo pipefail

SECRETS_FILE="$1"
. "$SECRETS_FILE"

function main {
    for file in ./conf/*; do
        backup_name="$(basename "$file")"
        backup_location="$(cat "$file")"
        backup_repo="${BASE_URL}/${BUCKET_NAME}/${backup_name}"
        export AWS_ACCESS_KEY_ID="$KEY_ID"
        export AWS_SECRET_ACCESS_KEY="$APP_KEY"

        echo "### ### $backup_name"

        echo "### checking repo exists"
        set +e
        ./bin/restic -r "$backup_repo" snapshots --insecure-no-password >/dev/null
        check_result=$?
        set -e

        if [ "$check_result" != 0 ]; then
            echo "### trying to init repo"
            ./bin/restic -r "$backup_repo" init --insecure-no-password
        fi

        echo "### backing up"
        set +e
        ./bin/restic -r "$backup_repo" backup \
            --skip-if-unchanged \
            --insecure-no-password \
            "$backup_location"
        backup_result=$?
        set -e

        if [ "$backup_result" == 0 ]; then
            send_telegram_message "[$(hostname)] [${backup_name}] ✅ Backup Succeeded"
        else
            send_telegram_message "[$(hostname)] [${backup_name}] 🔴 Backup Failed"
        fi
    done
}

function send_telegram_message {
    curl -X POST \
        -H 'Content-Type: application/json' \
        -d '{"chat_id": "'"${TELEGRAM_CHAT_ID}"'", "text": "'"${1}"'"}' \
        "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage"
}

main "$@"
