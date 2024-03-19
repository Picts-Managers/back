from flask import request

from middlewares import schema
from middlewares.auth import isLogged
from models.User import User
from repositories import user_repository
from schemas.auth import login, register
from utils import route
from utils.auth import encrypt_password, generate_token


@route("/register")
@schema(register)
def register():
    username = request.body.username
    password = request.body.password
    email = request.body.email

    hashed_password = encrypt_password(password)

    new_user = User(
        username=username, password=hashed_password.decode("utf-8"), email=email
    )

    created_user = user_repository.insertUser(new_user)

    return {"access_token": generate_token(created_user.id)}


@route("/login")
@schema(login)
def login():
    login = request.body.login
    password = request.body.password

    if "@" in login:
        user = user_repository.getUserByEmailAndPassword(
            user_email=login, password=password
        )
    else:
        user = user_repository.getUserByUsernameAndPassword(
            user_username=login, password=password
        )

    return {"access_token": generate_token(user.id)}


@route("/login-with-token")
@isLogged
def login_with_token():
    return request.req_user
