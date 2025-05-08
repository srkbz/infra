#!/usr/bin/env bash
set -xeuo pipefail

build_id="$(openssl rand -hex 16)"
build_workspace="${SITE_STATE}/builds/${build_id}"

target_commit="$(cat "${SITE_TARGET_COMMIT}")"

repository="$(yq -re '.repository' "${SITE_CONFIG}")"
build_script="$(yq -re '.build.script // ""' "${SITE_CONFIG}")"
build_output="$(yq -re '.build.output // ""' "${SITE_CONFIG}")"

mkdir -p "${build_workspace}"

(
    cd "${build_workspace}"
    git init
    git remote add origin "${repository}"
    git fetch --tags origin "${target_commit}"
    git reset --hard "${target_commit}"

    if [ "${build_script}" != "" ]; then
        bash -c "$build_script"
        rm -rf "${SITE_LIVE}"
        cp -r "$build_output" "${SITE_LIVE}"
    elif [ -f "Dockerfile" ]; then
        docker build -t "static_site_${build_id}" .
        container_id=$(docker create "static_site_${build_id}")
        rm -rf "${SITE_LIVE}"
        docker cp "${container_id}:/dist" "${SITE_LIVE}"
        docker rm -f "${container_id}"
        docker rmi "static_site_${build_id}"
    else
        rm -rf "${SITE_LIVE}"
        cp -r "dist" "${SITE_LIVE}"
    fi

    printf "%s" "${target_commit}" >"${SITE_LIVE_COMMIT}"
)

rm -rf "${build_workspace}"
