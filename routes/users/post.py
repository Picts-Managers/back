from flask import request
from repositories import user_repository
from models.User import User


def index():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    token = "7667AZZA"

    new_user = User(username=username, password=password, email=email, token=token)

    created_user = user_repository.insertUser(new_user)

    return created_user.model_dump()
