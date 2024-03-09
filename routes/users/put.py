from flask import request
from bson import ObjectId
from models.User import User
from repositories import user_repository
from utils import route


@route("/")
def update(user_id: str):
    _user_id = ObjectId(user_id)

    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")

    new_user = User(username=username, password=password, email=email)

    updated_user = user_repository.updateUser(_user_id, new_user)
    del updated_user.password
    return updated_user
