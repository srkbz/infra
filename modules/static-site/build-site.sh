#!/usr/bin/env bash
set -xeuo pipefail

BUILD_ID="$(openssl rand -hex 16)"
BUILD_WORKSPACE="${SITE_HOME}/builds/${BUILD_ID}"
SITE_LIVE="${SITE_HOME}/live"
TARGET_COMMIT="$(cat "${SITE_HOME}/TARGET_COMMIT")"

mkdir -p "${BUILD_WORKSPACE}"

(
    cd "${BUILD_WORKSPACE}"
    git init
    git remote add origin "${REPOSITORY}"
    git fetch origin "${TARGET_COMMIT}"
    git reset --hard "${TARGET_COMMIT}"

    if [ "$DOMAIN" == "ebro.sirikon.me" ]; then
        ./meta/docker/build.sh website
        rm -rf "${SITE_LIVE}"
        cp -r "out/website" "${SITE_LIVE}"
    elif [ -f "Dockerfile" ]; then
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
    printf "%s" "${TARGET_COMMIT}" >"${SITE_HOME}/LIVE_COMMIT"
)

rm -rf "${BUILD_WORKSPACE}"
