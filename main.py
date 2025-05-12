#!/usr/bin/env python3
import os
import importlib

from framework.runner import runner

for module in os.listdir(os.path.join(os.path.dirname(__file__), "modules")):
    importlib.import_module("modules." + module)


runner.run()
