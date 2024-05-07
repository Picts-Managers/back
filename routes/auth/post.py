from flask import Blueprint, abort, request

from middlewares import schema
from middlewares.auth import isLogged
from models.User import User
from repositories import user_repository
from schemas.auth import login, register
from utils.auth import encrypt_password, generate_token

blueprint = Blueprint(__name__.replace(".", "/"), __name__)


@blueprint.post("/register")
@schema(register)
def register_req():
    username = request.body.username
    password = request.body.password
    email = request.body.email

    hashed_password = encrypt_password(password)

    new_user = User(
        username=username, password=hashed_password.decode("utf-8"), email=email
    )

    if user_repository.getUserByEmail(
        new_user.email
    ) or user_repository.getUserByUsername(new_user.username):
        return abort(400, "User already exists")

    created_user = user_repository.insertUser(new_user)

    return {"access_token": generate_token(created_user.id)}


@blueprint.post("/login")
@schema(login)
def login_req():
    login = request.body.login.lower()
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


@blueprint.post("/login-with-token")
@isLogged
def login_with_token():
    return request.req_user
