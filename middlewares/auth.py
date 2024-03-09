from functools import wraps
from flask import request
import logging

__logger = logging.getLogger(__name__)


def isLoggedIn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        __logger.info("isLoggedIn")
        return func(*args, **kwargs)

    return wrapper
