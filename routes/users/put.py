from flask import request

from middlewares.auth import isLogged
from models.User import User
from repositories import user_repository
from schemas.users import userUpdate
from utils import route, schema


@route("/me")
@isLogged
@schema(userUpdate)
def update():
    username = request.body.username
    email = request.body.email

    new_user = User(username=username, email=email)

    updated_user = user_repository.updateUser(request.req_user, new_user)
    del updated_user.password
    return updated_user
