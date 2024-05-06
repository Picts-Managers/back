from flask import Blueprint, request

from middlewares import schema
from middlewares.auth import isLogged
from schemas.users import getUser

blueprint = Blueprint(__name__.replace(".", "/"), __name__)


@blueprint.get("/me")
@isLogged
@schema(getUser)
def index():
    return request.req_user
