from flask import g, request
from bson import ObjectId
from middlewares.auth import isLogged
from models.User import User
from repositories import user_repository
from utils import route


@route("/me")
@isLogged
def update():
    # _user_id = ObjectId(user_id)
    # # new_user = User()

    # body = request.json
    # match body:
    #     case "username":
    #         new_user = User(username=body)
    #     case "password":
    #         new_user = User(password=body)
    #     case "email":
    #         new_user = User(email=body)

    # updated_user = user_repository.updateUser(_user_id, new_user)
    # del updated_user.password
    # return updated_user
    return g.req_user
