import os

import bcrypt
import jwt
from bson import ObjectId
from flask import g, request, abort
from middlewares.auth import isLogged
from repositories import user_repository
from models.User import User
from utils import route
from utils.auth import check_token, encrypt_password, generate_token




@route("/register")
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")

    hashed_password = encrypt_password(password)

    new_user = User(username=username, password=hashed_password.decode("utf-8"), email=email)

    created_user = user_repository.insertUser(new_user)

    return { 'access_token': generate_token(created_user.id)}


@route("/login")
def login():
    login = request.json.get("login")
    password = request.json.get("password")

    if "@" in login:
        user = user_repository.getUserByEmailAndPassword(user_email=login, password=password)
    else:
        user = user_repository.getUserByUsernameAndPassword(user_username=login, password=password)

    return { 'access_token': generate_token(user.id) }


@route("/login-with-token")
@isLogged
def login_with_token():
    return g.req_user