import os

import bcrypt
from bson import ObjectId
from flask import abort

from models.User import User
from utils.db import client


class __UserRepository:
    def __init__(self):
        self.collection = client[os.getenv("DB_NAME")].users

    def getUsers(self) -> list[User]:
        return [User(**user) for user in self.collection.find({}) if user is not None]

    def getUserById(self, user_id: ObjectId) -> User:
        user = self.collection.find_one({"_id": user_id})
        return User(**user) if user else None

    def getUserByEmail(self, user_email: str) -> User:
        user = self.collection.find_one({"email": user_email})
        return User(**user) if user else None

    def getUserByEmailAndPassword(self, user_email: str, password: str) -> User:
        user = self.collection.find_one({"email": user_email})
        if user:
            stored_password = user["password"].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), stored_password):
                return User(**user)
            else:
                return abort(401, description="wrong_password")
        return abort(401, description="user_not_found")

    def getUserByUsernameAndPassword(self, user_username: str, password: str) -> User:
        user = self.collection.find_one({"username": user_username})
        if user:
            stored_password = user["password"].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), stored_password):
                return User(**user)
        return abort(401, description="user_not_found")

    def insertUser(self, new_user: User):
        result = self.collection.insert_one(new_user.model_dump())
        inserted_user = self.collection.find_one({"_id": result.inserted_id})
        return User(**inserted_user) if inserted_user else None

    def updateUser(self, user_id: ObjectId, new_user: User):
        self.collection.update_one({"_id": user_id}, {"$set": new_user.model_dump()})
        updated_user = self.collection.find_one({"_id": user_id})
        return User(**updated_user) if updated_user else None

    def deleteUser(self, user_id: ObjectId):
        return self.collection.delete_one({"_id": user_id})


user_repository = __UserRepository()
