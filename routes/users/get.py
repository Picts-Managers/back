from flask import request

from middlewares.auth import isLogged
from utils import route


@route("/me")
@isLogged
def index():
    return request.req_user
