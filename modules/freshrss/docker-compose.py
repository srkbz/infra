#!/usr/bin/env python3
import json
import os

FRESHRSS_HOME = os.environ.get("FRESHRSS_HOME")
FRESHRSS_HOSTS = os.environ.get("FRESHRSS_HOSTS")

hosts = FRESHRSS_HOSTS.split(",")
with open(os.environ.get("FRESHRSS_PORT_FILE"), "r") as f:
    port = f.read().strip()

print(
    json.dumps(
        {
            "services": {
                "freshrss": {
                    "image": "freshrss/freshrss",
                    "restart": "always",
                    "labels": {"com.centurylinklabs.watchtower.enable": "true"},
                    "environment": {"TZ": "Europe/Madrid", "CRON_MIN": "15,45"},
                    "volumes": [f"{FRESHRSS_HOME}:/var/www/FreshRSS/data"],
                    "ports": [f"{host}:{port}:80" for host in hosts],
                }
            }
        },
        indent=2,
    )
)
