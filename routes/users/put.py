from flask import request

from middlewares import schema
from middlewares.auth import isLogged
from repositories import user_repository
from schemas.users import userUpdate
from utils import route


@route("/me")
@isLogged
@schema(userUpdate)
def update_user():
    updated_user = user_repository.updateUser(request.req_user.id, request.body)
    del updated_user.password
    return updated_user
