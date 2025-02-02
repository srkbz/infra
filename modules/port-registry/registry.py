#!/usr/bin/env python3
import json
import sys
import os
import os.path

PORT_REGISTRY_HOME = os.environ.get("PORT_REGISTRY_HOME")
DB_PATH = os.path.join(PORT_REGISTRY_HOME, "db.json")

db = {"ports": {}, "task_ids": {}, "next_port": 10000}


def main():
    read_db()
    args = sys.argv[1:]
    match args:
        case ["reserve", task_id]:
            reserve(task_id, next())
        case ["reserve", task_id, port]:
            reserve(task_id, port)
        case ["get-port", task_id]:
            print(f"get port for {task_id}")
    write_db()


def reserve(task_id, port):
    db["task_ids"][task_id] = port
    db["ports"][port] = task_id


def next_port():
    r = db["next_port"]
    db["next_port"] = db["next_port"] + 1
    return r


def get_port(task_id):
    if task_id not in db["task_ids"]:
        print(f"Task {task_id} has no port assigned")
        exit(1)


def read_db():
    global db
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            db = json.loads(f.read())


def write_db():
    with open(DB_PATH, "w") as f:
        f.write(json.dumps(db, indent=2))


main()
