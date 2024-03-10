import os

import jwt
from bson import ObjectId
from flask import request, abort
from repositories import user_repository
from utils import route
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@route("/login-with-token")
def index():
    token = request.headers.get("Authorization")

    if token is None:
        return abort(401, description="missing_token")

    try:
        token = token.replace("Bearer ", "")
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_token.get("id")
        _user_id = ObjectId(user_id)

        if user_id:
            user = user_repository.getUserById(_user_id)

            if user:
                del user.password
                return user

    except jwt.ExpiredSignatureError:
        return abort(401, description="expired_token")
    except jwt.InvalidTokenError:
        return abort(401, description="invalid_token")

    return abort(401, description="invalid_token")
