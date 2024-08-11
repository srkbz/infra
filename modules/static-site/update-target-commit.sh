#!/usr/bin/env bash
set -xeuo pipefail

BUILD_ID="$(openssl rand -hex 16)"
BUILD_WORKSPACE="/srv/srkbz/static-sites/${DOMAIN}/builds/${BUILD_ID}"

mkdir -p "${BUILD_WORKSPACE}"

(
    cd "${BUILD_WORKSPACE}"
    git init
    git remote add origin "${REPOSITORY}"
    git fetch origin "${BRANCH}"
    git rev-parse origin/"${BRANCH}" \
        >"/srv/srkbz/static-sites/${DOMAIN}/COMMIT"
)

rm -rf "${BUILD_WORKSPACE}"
