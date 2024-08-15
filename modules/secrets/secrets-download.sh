#!/usr/bin/env bash
set -euo pipefail

rm -rf ./*
chmod 700 .
umask 077
curl -Lo "secrets.zip" "${SECRETS_URL}"
unzip -o 'secrets.zip' || true
echo "${SECRETS_PASSWORD}" | keepassxc-cli export --quiet secrets.kdbx >secrets.xml
