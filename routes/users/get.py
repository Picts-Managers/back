import logging
from bson import ObjectId
from flask import abort, g

from middlewares.auth import isLogged
from repositories import user_repository
from utils import route


@route("/me")
@isLogged
def index():
    return g.req_user
