#!/usr/bin/env bash
set -euo pipefail

arch="$(dpkg --print-architecture)"
version="$(. /etc/os-release && echo "$VERSION_CODENAME")"
keyring="/etc/apt/keyrings/docker.asc"
keyrings_dir="$(dirname "$keyring")"

install -m 0755 -d "$keyrings_dir"
curl -fsSL https://download.docker.com/linux/debian/gpg -o "$keyring"
chmod a+r "$keyring"

echo \
  "deb [arch=${arch} signed-by=${keyring}] https://download.docker.com/linux/debian ${version} stable" |
  tee /etc/apt/sources.list.d/docker.list >/dev/null
