#!/usr/bin/env python3
import random
from os import environ, makedirs
from os.path import join, isfile, dirname
import string
from subprocess import run, PIPE
import json

ACCESS_KEY_ID = environ.get("ACCESS_KEY_ID")
SECRET_ACCESS_KEY = environ.get("SECRET_ACCESS_KEY")
BUCKET = environ.get("BUCKET")
ENDPOINT = environ.get("ENDPOINT")

query = 'tasks | filter(any(keys(.labels), # startsWith "litestream.")) | map([.id, .labels]) | toJSON()'
query_cmd = run(
    [environ.get("EBRO_BIN"), "-i", "--query", query],
    cwd=environ.get("EBRO_ROOT"),
    stdout=PIPE,
)

data: list[tuple[str, dict[str, str]]] = json.loads(query_cmd.stdout.decode("utf-8"))


result = {
    "access-key-id": ACCESS_KEY_ID,
    "secret-access-key": SECRET_ACCESS_KEY,
    "dbs": [],
}


for task_id, labels in data:
    for label in labels.keys():
        if label.startswith("litestream."):
            db_name = label.removeprefix("litestream.")
            db_path = labels[label]

            result["dbs"].append(
                {
                    "path": db_path,
                    "replicas": [
                        {
                            "type": "s3",
                            "bucket": BUCKET,
                            "path": f"litestream/{task_id}/{db_name}",
                            "endpoint": ENDPOINT,
                            "force-path-style": True,
                        }
                    ],
                }
            )

print(json.dumps(result, indent=2))
