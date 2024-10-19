#!/usr/bin/env bash
set -euo pipefail

# Add missing CA
curl 'https://cacerts.digicert.com/ThawteTLSRSACAG1.crt.pem' >/usr/local/share/ca-certificates/ThawteTLSRSACAG1.crt
update-ca-certificates

exec node server/server.js
