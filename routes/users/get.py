import logging
from bson import ObjectId
from flask import abort

from repositories import user_repository
from utils import route


@route("/")
def index():
    user = user_repository.getUsers()
    for u in user:
        del u.password
    return user


@route("/<user_id>")
def index(user_id: str):
    _user_id = ObjectId(user_id)
    user = user_repository.getUserById(_user_id)
    if not len(user):
        abort(404, description="User not found")
    user = user[0]
    del user.password
    return user
