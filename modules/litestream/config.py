#!/usr/bin/env python3
import random
from os import environ
from os.path import join, isfile
import string
from subprocess import run, PIPE
import json

LITESTREAM_CACHE = environ.get("LITESTREAM_CACHE")

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


def task_generation(task_id: str):
    generation_file = join(LITESTREAM_CACHE, "generations", task_id)
    if isfile(generation_file):
        with open(generation_file, "r") as f:
            return f.read()
    else:
        generation = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=16)
        )
        with open(generation_file, "w") as f:
            return f.write(generation)
        return generation


for task_id, labels in data:
    for label in labels.keys():
        if label.startswith("litestream."):
            db_name = label.removeprefix("litestream.")
            db_path = labels[label]
            generation = task_generation(task_id)

            result["dbs"].append(
                {
                    "path": db_path,
                    "replicas": [
                        {
                            "type": "s3",
                            "bucket": BUCKET,
                            "path": f"litestream/{task_id}/{generation}/{db_name}",
                            "endpoint": ENDPOINT,
                            "force-path-style": True,
                        }
                    ],
                }
            )

print(json.dumps(result, indent=2))
