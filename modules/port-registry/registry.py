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
    match sys.argv[1:]:
        case ["reserve", task_id]:
            reserve(task_id, next_available_port())
        case ["reserve", task_id, port]:
            reserve(task_id, port)
        case ["get-port", task_id]:
            print(get_port(task_id))
    write_db()


def reserve(task_id, port):
    if port in db["ports"] and db["ports"][port] != task_id:
        current_task_id = db["ports"][port]
        raise Exception(f"Port {port} is already reserved to {current_task_id}")

    if task_id in db["task_ids"]:
        old_port = db["task_ids"][task_id]
        db["ports"].pop(old_port)
        db["task_ids"].pop(task_id)

    db["task_ids"][task_id] = port
    db["ports"][port] = task_id


def next_available_port():
    while True:
        port = db["next_port"]
        db["next_port"] = db["next_port"] + 1
        if port not in db["ports"]:
            return port


def get_port(task_id):
    if task_id not in db["task_ids"]:
        print(f"Task {task_id} has no port assigned")
        exit(1)
    return db["task_ids"][task_id]


def read_db():
    global db
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            db = json.loads(f.read())


def write_db():
    with open(DB_PATH, "w") as f:
        f.write(json.dumps(db, indent=2))


main()
