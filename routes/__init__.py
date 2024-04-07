import importlib
import os
import logging

from utils import app


__logger = logging.getLogger("router_init")

__logger.info("Initializing Routes:")
for root, folders, files in os.walk("./routes", topdown=False):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            module = importlib.import_module(
                f"{root[2:]}.{file[:-3]}".replace("/", ".")
            )

__logger.info("Routes Initialized")
