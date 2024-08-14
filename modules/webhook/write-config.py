#!/usr/bin/env python3
import json
from os import listdir
from os.path import isdir, join

webhooks = []

if isdir(".cache/webhook/conf"):
    for item in listdir(".cache/webhook/conf"):
        item_path = join(".cache/webhook/conf", item)
        with open(item_path, "r") as f:
            webhooks = [*webhooks, *json.load(f)]

with open("/etc/webhook.conf", "w") as f:
    json.dump(f, indent=2)
