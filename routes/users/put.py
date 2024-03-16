from flask import abort, g, request
from bson import ObjectId
from middlewares.auth import isLogged
from models.User import User
from repositories import user_repository
from utils import route


@route("/me")
@isLogged
def update():
    body: dict = request.json

    if not body:
        return abort(400, "Invalid request")

    username = body.get("username")
    password = body.get("password")
    email = body.get("email")

    new_user = User(username=username, password=password, email=email)

    updated_user = user_repository.updateUser(g.req_user, new_user)
    del updated_user.password
    return updated_user
