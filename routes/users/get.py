import logging
from bson import ObjectId
from flask import abort
from pydantic import BaseModel

from repositories import user_repository
from utils import route


@route("/")
def index():
    user = user_repository.getUsers()
    return user


@route("/<user_id>")
def index(user_id: str):
    _user_id = ObjectId(user_id)
    user = user_repository.getUser(_user_id)
    if not len(user):
        abort(404, description="User not found")
    user = user[0]
    return user
