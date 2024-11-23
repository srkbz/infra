#!/usr/bin/env python3

import json
from os import environ, makedirs, getcwd
from os.path import dirname

DOMAIN = environ.get("DOMAIN")
BRANCH = environ.get("BRANCH")
WEBHOOK_SECRET = environ.get("WEBHOOK_SECRET")
SITE_HOME = environ.get("SITE_HOME")
SITE_WEBHOOK_CONF = environ.get("SITE_WEBHOOK_CONF")

if WEBHOOK_SECRET is None:
    raise Exception("WEBHOOK_SECRET is not configured")

makedirs(dirname(SITE_WEBHOOK_CONF), exist_ok=True)
with open(SITE_WEBHOOK_CONF, "w") as f:
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
