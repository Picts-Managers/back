import importlib
from json import JSONEncoder
import os
from flask import Flask
import inspect
import logging

app = Flask(__name__)

__logger = logging.getLogger("router_init")

__logger.info("Initializing Routes:")
for root, folders, files in os.walk("./routes", topdown=False):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            module = importlib.import_module(
                f"{root[2:]}.{file[:-3]}".replace("/", ".")
            )
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj):
                    route = f"{root[8:]}/{f'{name}/' if name != 'index' else ''}"
                    params = inspect.signature(obj).parameters
                    route += "/".join([f"<{param}>" for param in params])
                    __logger.info(f"  {file[:-3].upper()} {route}")
                    app.add_url_rule(
                        route,
                        route,
                        view_func=obj,
                        methods=[file[:-3].upper()],
                    )

__logger.info("Routes Initialized")

from utils import MongoJSONProvider

app.json = MongoJSONProvider(app)
