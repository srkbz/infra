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

echo "${KERNEL_MAP["$(uname -s)"]}_${ARCH_MAP["$(uname -m)"]}"
