from functools import wraps
from flask import abort, request, g
import logging

from repositories import user_repository
from utils.auth import check_token

__logger = logging.getLogger(__name__)


def isLogged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return abort(401, "unauthorized")

        user_id = check_token(token[7:])

        if not user_id:
            return abort(401, "unauthorized")

        try:
            user = user_repository.getUserById(user_id)
        except Exception as e:
            return abort(401, "unauthorized")

        del user.password
        g.req_user = user
        return func(*args, **kwargs)

    return wrapper
