import os

import bcrypt
import jwt
from flask import request
from repositories import user_repository
from models.User import User
from utils import route

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@route("/sign-up")
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


@route("/sign-in")
def index():
    login = request.json.get("login")
    password = request.json.get("password")

    if "@" in login:
        user = user_repository.getUserByEmail(login)
    else:
        user = user_repository.getUserByUsername(login)

    if not user:
        return "user_not_found"

    stored_password = user.password.encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
        payload = {"id": str(user.id)}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        user.token = token
        user_repository.updateUser(user.id, user)
        del user.password
        return user

    return "wrong_password"
