#!/usr/bin/env bash
set -euo pipefail

# Add missing CA
curl 'https://cacerts.digicert.com/ThawteTLSRSACAG1.crt.pem' >/usr/local/share/ca-certificates/ThawteTLSRSACAG1.crt
update-ca-certificates

export NODE_EXTRA_CA_CERTS="/usr/local/share/ca-certificates/ThawteTLSRSACAG1.crt"
exec node server/server.js
