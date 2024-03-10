import os

import bcrypt
import jwt
from bson import ObjectId
from flask import request, abort
from repositories import user_repository
from models.User import User
from utils import route

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@route("/register")
def index():
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")

    salt = bcrypt.gensalt()
    bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(bytes, salt)

    new_user = User(username=username, password=hashed_password.decode("utf-8"), email=email)

    created_user = user_repository.insertUser(new_user)

    payload = {"id": str(created_user.id)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    created_user.token = token
    created_user_with_token = user_repository.updateUser(created_user.id, created_user)

    del created_user_with_token.password
    return created_user_with_token


@route("/login")
def index():
    login = request.json.get("login")
    password = request.json.get("password")

    if "@" in login:
        user = user_repository.getUserByEmailAndPassword(user_email=login, password=password)
    else:
        user = user_repository.getUserByUsernameAndPassword(user_username=login, password=password)

    payload = {"id": str(user.id)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    user.token = token
    user_repository.updateUser(user.id, user)
    del user.password
    return user


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
