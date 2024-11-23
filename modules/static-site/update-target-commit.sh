#!/usr/bin/env bash
set -xeuo pipefail

BUILD_ID="$(openssl rand -hex 16)"
BUILD_WORKSPACE="${SITE_HOME}/builds/${BUILD_ID}"

mkdir -p "${BUILD_WORKSPACE}"

(
    cd "${BUILD_WORKSPACE}"
    git init
    git remote add origin "${REPOSITORY}"
    git fetch origin "${BRANCH}"
    TARGET_COMMIT="$(git rev-parse origin/"${BRANCH}")"
    printf "%s" "${TARGET_COMMIT}" >"${SITE_HOME}/TARGET_COMMIT"
)

rm -rf "${BUILD_WORKSPACE}"
