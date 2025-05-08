#!/usr/bin/env bash
set -xeuo pipefail

build_id="$(openssl rand -hex 16)"
build_workspace="${SITE_STATE}/builds/${build_id}"

repository="$(yq -re '.repository' "${SITE_CONFIG}")"
branch="$(yq -re '.branch // "master"' "${SITE_CONFIG}")"

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
