from bson import ObjectId
from utils.db import client
import os
from models.User import User


class __UserRepository:
    def __init__(self):
        self.collection = client[os.getenv("DB_NAME")].users

    def getUsers(self) -> list[User]:
        return [User(**user) for user in self.collection.find({}) if user is not None]

    def getUser(self, user_id: ObjectId) -> list[User]:
        return [
            User(**user)
            for user in self.collection.find({"_id": user_id})
            if user is not None
        ]

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
