import os

import jwt
from bson import ObjectId
from flask import request
from repositories import user_repository
from utils import route
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@route("/sign-in-with-token")
def sign_in_with_token():
    token = request.headers.get("Authorization")

    if token is None:
        return "missing_token", 401

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
        return "expired_token", 401
    except jwt.InvalidTokenError:
        return "invalid_token", 401

    return "invalid_token", 401
