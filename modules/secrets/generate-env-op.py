#!/usr/bin/env python3
from os import environ
from os.path import join
from subprocess import run, PIPE
from sys import argv
import json

SECRETS_HOME = environ.get("SECRETS_HOME")

with open(join(SECRETS_HOME, "secrets.json"), "r") as f:
    secrets = json.load(f)

task_id = environ.get("EBRO_TASK_ID")

expr = f'filter(tasks, .id == "{task_id}")[0].labels | toJSON()'
labels_cmd = run(
    [environ.get("EBRO_BIN"), "-i", "--query", expr],
    cwd=environ.get("EBRO_ROOT"),
    stdout=PIPE,
)

labels = json.loads(labels_cmd.stdout.decode("utf-8"))

for key, value in enumerate(labels):
    if key.startswith("secret."):
        print(key)
        print(value)
