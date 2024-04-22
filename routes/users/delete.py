from flask import request

from middlewares.auth import isLogged
from repositories import user_repository
from utils.routeDecorator import route


@route("/me")
@isLogged
def get_user():
    user_repository.deleteUser(request.req_user.id)

    return True
