from flask import request
from middlewares.auth import isLogged
from models.User import User
from repositories import user_repository
from utils import route


@route("/me")
@isLogged
def update():
    username = request.body.username
    password = request.body.password
    email = request.body.email

    new_user = User(username=username, password=password, email=email)

    updated_user = user_repository.updateUser(request.req_user, new_user)
    del updated_user.password
    return updated_user
