#!/usr/bin/env bash
set -xeuo pipefail

eval "$("${EBRO_TASK_WORKING_DIRECTORY}/scripts/config.py")"

build_id="$(openssl rand -hex 16)"
build_workspace="${SITE_STATE}/builds/${build_id}"

mkdir -p "${build_workspace}"

(
    cd "${build_workspace}"
    git init
    git remote add origin "${repository}"
    git fetch origin "${branch}"
    target_commit="$(git rev-parse origin/"${branch}")"
    printf "%s" "${target_commit}" >"${SITE_TARGET_COMMIT}"
)

rm -rf "${build_workspace}"
