import inspect
import logging
from utils import app

__logger = logging.getLogger("router_init")


def __getFilePath(func):
    module = inspect.getmodule(func)
    return module.__file__


def route(route: str):
    def route_wrapper(func):
        file_path = __getFilePath(func).split("routes")[-1]
        method = file_path.split("/")[-1][:-3].upper()
        path = f"{'/'.join(file_path.split('/')[:-1])}{route}"
        __logger.info(f"  {method} {path}")
        app.add_url_rule(
            path,
            method + path,
            view_func=func,
            methods=[method],
        )
        return func

    return route_wrapper
