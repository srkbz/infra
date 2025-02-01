#!/usr/bin/env bash
set -euo pipefail

tasks_with_cron="$(cd "${EBRO_ROOT}" && ${EBRO_BIN} -i --query 'tasks | filter("cron" in .labels) | map(.id) | join("\n")')"
for task_id in ${tasks_with_cron}; do
    task_cron="$(cd "${EBRO_ROOT}" && ${EBRO_BIN} -i --query "filter(tasks, .id == '${task_id}')[0].labels.cron")"
    echo "${task_cron} cd '${EBRO_ROOT}' && '${EBRO_BIN}' ${task_id}"
done
