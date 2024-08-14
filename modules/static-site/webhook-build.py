#!/usr/bin/env python3

import json
from os import environ, makedirs

DOMAIN = environ.get("DOMAIN")
BRANCH = environ.get("BRANCH")
WEBHOOK_SECRET = environ.get("WEBHOOK_SECRET")
TASKFILE_DIR = environ.get("TASKFILE_DIR")
SRKBZ_INFRA_ROOT = environ.get("SRKBZ_INFRA_ROOT")

if WEBHOOK_SECRET is None:
    raise Exception("WEBHOOK_SECRET is not configured")

makedirs(".cache/webhook/conf", exist_ok=True)
with open(f".cache/webhook/conf/static-site_{DOMAIN}.json", "w") as f:
    json.dump(
        [
            {
                "id": f"static-site/{DOMAIN}",
                "execute-command": f"{TASKFILE_DIR}/webhook-run.sh",
                "pass-arguments-to-command": [{"source": "string", "name": DOMAIN}],
                "command-working-directory": SRKBZ_INFRA_ROOT,
                "trigger-rule": {
                    "and": [
                        {
                            "match": {
                                "type": "payload-hmac-sha1",
                                "secret": WEBHOOK_SECRET,
                                "parameter": {
                                    "source": "header",
                                    "name": "X-Hub-Signature",
                                },
                            }
                        },
                        {
                            "match": {
                                "type": "value",
                                "value": f"refs/heads/{BRANCH}",
                                "parameter": {"source": "payload", "name": "ref"},
                            }
                        },
                    ]
                },
            }
        ],
        f,
        indent=2,
    )
    f.write("\n")
