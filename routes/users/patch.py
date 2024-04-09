from flask import request

from middlewares import schema
from middlewares.auth import isLogged
from models.User import User
from repositories import user_repository
from schemas.users import userUpdate
from utils import route


@route("/me")
@isLogged
@schema(userUpdate)
def update():
    username = (
        request.body.username if request.body.username else request.req_user.username
    )
    email = request.body.email if request.body.email else request.req_user.email
    new_user = User(username=username, email=email)

    updated_user = user_repository.updateUser(request.req_user, new_user)
    del updated_user.password
    return updated_user
