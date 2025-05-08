#!/usr/bin/env python3
import json
import os
import os.path

SITE_CONFIG = os.environ.get("SITE_CONFIG")

with open(SITE_CONFIG, "r") as f:
    data = json.loads(f.read())

print("repository='" + data["repository"] + "'")
print("branch='" + (data["branch"] if "branch" in data else "master") + "'")
print("build_script='" + ((data["build"]["script"] if "build" in data else "")) + "'")
print("build_output='" + ((data["build"]["output"] if "build" in data else "")) + "'")
