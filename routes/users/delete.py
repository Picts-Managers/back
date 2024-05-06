from flask import Blueprint, request

from middlewares.auth import isLogged
from repositories import user_repository

blueprint = Blueprint(__name__.replace(".", "/"), __name__)


@blueprint.delete("/me")
@isLogged
def get_user():
    user_repository.deleteUser(request.req_user.id)

    return True
