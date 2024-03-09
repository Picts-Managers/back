import os

import bcrypt
import jwt
from flask import request
from repositories import user_repository
from models.User import User
from utils import route

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@route("/")
def index():
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    new_user = User(username=username, password=hashed_password, email=email)

    created_user = user_repository.insertUser(new_user)

    payload = {"id": str(created_user.id)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    created_user.token = token
    created_user_with_token = user_repository.updateUser(created_user.id, created_user)

    del created_user_with_token.password
    return created_user_with_token
