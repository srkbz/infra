#!/usr/bin/env python3
import json
from os import listdir

webhooks = []

for item in listdir("."):
    with open(item, "r") as f:
        webhooks = [*webhooks, *json.load(f)]

with open("/etc/webhook.conf", "w") as f:
    json.dump(webhooks, f, indent=2)
    f.write("\n")
