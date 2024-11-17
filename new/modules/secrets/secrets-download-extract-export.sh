#!/usr/bin/env bash
set -euo pipefail

rm -rf ./*
chmod -R 700 .
umask 077
curl -Lo "secrets.zip" "${SECRETS_URL}"
unzip -o 'secrets.zip' || true
chmod 700 secrets.kdbx
echo "${SECRETS_PASSWORD}" | keepassxc-cli export --quiet secrets.kdbx >secrets.xml
