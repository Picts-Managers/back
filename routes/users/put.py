from flask import Blueprint, request

from middlewares import schema
from middlewares.auth import isLogged
from repositories import user_repository
from schemas.users import userUpdate

blueprint = Blueprint(__name__.replace(".", "/"), __name__)


@blueprint.put("/me")
@isLogged
@schema(userUpdate)
def update_user():
    updated_user = user_repository.updateUser(request.req_user.id, request.body)
    del updated_user.password
    return updated_user
