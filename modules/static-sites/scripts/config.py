#!/usr/bin/env python3
import json
import os
import os.path

SITE_HOME = os.environ.get("SITE_HOME")

with open(os.path.join(SITE_HOME, "config.json"), "r") as f:
    data = json.loads(f.read())

print("repository='" + data["repository"] + "'")
print("branch='" + (data["branch"] if "branch" in data else "master") + "'")
