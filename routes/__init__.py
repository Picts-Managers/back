import importlib
import os
import logging

from utils import app


__logger = logging.getLogger("router_init")


def init_routes():
    __logger.info("Initializing Routes:")
    for root, _, files in os.walk("./routes", topdown=False):
        for file in files:
            if root != "./routes" and file == "__init__.py":
                blueprint = importlib.import_module(
                    f"{root[2:]}".replace("/", ".")
                ).blueprint
                app.register_blueprint(blueprint)

    __logger.info("Routes Initialized")
