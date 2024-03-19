from flask import request

from middlewares import schema
from middlewares.auth import isLogged
from schemas.users import getUser
from utils import route


@route("/me")
@isLogged
@schema(getUser)
def index():
    return request.req_user
