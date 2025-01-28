#!/usr/bin/env bash
set -euo pipefail

declare -A KERNEL_MAP=(
    ["Linux"]="linux"
    ["Darwin"]="darwin"
)

declare -A ARCH_MAP=(
    ["x86_64"]="amd64"
    ["arm64"]="arm64"
)

kernel="$(uname -s)"
arch="$(uname -m)"

echo "${KERNEL_MAP["$kernel"]}_${ARCH_MAP["$arch"]}"
