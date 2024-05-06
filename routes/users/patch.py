from flask import Blueprint, abort, request

from middlewares import schema
from middlewares.auth import isLogged
from repositories import user_repository
from schemas.users import userUpdatePassword
from utils.auth import encrypt_password, verify_password

blueprint = Blueprint(__name__.replace(".", "/"), __name__)


@blueprint.patch("/me")
@isLogged
@schema(userUpdatePassword)
def update_password():
    user = user_repository.getUserById(request.req_user.id)
    if verify_password(request.body.old_password, user.password):
        user.password = encrypt_password(request.body.new_password).decode("utf8")
        updated_user = user_repository.updateUser(user.id, user)
    else:
        return abort(401, description="wrong_password")
    del updated_user.password
    return updated_user
