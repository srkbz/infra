#!/usr/bin/env python3
import json
from os import environ, listdir
from subprocess import PIPE, run

expr = f'tasks | filter("webhook.conf" in .labels) | map(.labels["webhook.conf"]) | toJSON()'
query_cmd = run(
    [environ.get("EBRO_BIN"), "-i", "--query", expr],
    cwd=environ.get("EBRO_ROOT"),
    stdout=PIPE,
)

conf_files: list[str] = json.loads(query_cmd.stdout.decode("utf-8"))

webhooks = []

for conf_file in conf_files:
    with open(conf_file, "r") as f:
        webhooks = [*webhooks, *json.load(f)]

json.dumps(webhooks, indent=2)
