#!/usr/bin/env python3

import json
from sys import argv
from os import environ, getcwd

DOMAIN = environ.get("DOMAIN")
BRANCH = environ.get("BRANCH")
WEBHOOK_SECRET = environ.get("WEBHOOK_SECRET")
SITE_HOME = environ.get("SITE_HOME")

if WEBHOOK_SECRET is None:
    raise Exception("WEBHOOK_SECRET is not configured")

with open(argv[1], "w") as f:
    json.dump(
        [
            {
                "id": f"static-site/{DOMAIN}",
                "execute-command": f"{getcwd()}/webhook-run.sh",
                "pass-arguments-to-command": [{"source": "string", "name": SITE_HOME}],
                "command-working-directory": getcwd(),
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
