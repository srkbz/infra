#!/usr/bin/env bash
set -xeuo pipefail

BUILD_ID="$(openssl rand -hex 16)"
BUILD_WORKSPACE="/srv/srkbz/static-sites/${DOMAIN}/builds/${BUILD_ID}"
SITE_LIVE="/srv/srkbz/static-sites/${DOMAIN}/live"

mkdir -p "${BUILD_WORKSPACE}"

(
    cd "${BUILD_WORKSPACE}"
    git init
    git remote add origin "${REPOSITORY}"
    git fetch origin "${COMMIT}"
    git reset --hard "${COMMIT}"

    if [ -f "Dockerfile" ]; then
        docker build -t "site_${BUILD_ID}" .
        container_id=$(docker create "site_${BUILD_ID}")
        rm -rf "${SITE_LIVE}"
        docker cp "${container_id}:/dist" "${SITE_LIVE}"
        docker rm -f "${container_id}"
        docker rmi "site_${BUILD_ID}"
    else
        rm -rf "${SITE_LIVE}"
        cp -r "dist" "${SITE_LIVE}"
    fi
    printf "%s" "${COMMIT}" >"/srv/srkbz/static-sites/${DOMAIN}/COMMIT"
)

rm -rf "${BUILD_WORKSPACE}"
