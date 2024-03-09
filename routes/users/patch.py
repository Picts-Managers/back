from flask import request
from bson import ObjectId
from models.User import User
from repositories import user_repository
from utils import route


@route("/")
def update(param: str, user_id: str):
    _user_id = ObjectId(user_id)
    new_user = User()

    body = request.json.get(param)

    match param:
        case "username":
            new_user = User(username=body)
        case "password":
            new_user = User(password=body)
        case "email":
            new_user = User(email=body)

    updated_user = user_repository.updateUser(_user_id, new_user)
    del updated_user.password
    return updated_user
