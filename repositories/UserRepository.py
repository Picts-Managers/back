from bson import ObjectId
from utils.db import client
import os
from models.User import User


class __UserRepository:
    def __init__(self):
        self.collection = client[os.getenv("DB_NAME")].users

    def getUser(self, user_id: ObjectId) -> list[User]:
        return [
            User(**user)
            for user in self.collection.find({"_id": user_id})
            if user is not None
        ]


    def insertUser(self, new_user: User):
        return self.collection.insert_one(new_user.model_dump())

    def updateUser(self, user_id: ObjectId, new_user: User):
        return self.collection.update_one(
            {"_id": user_id}, {"$set": new_user.model_dump()}
        )

    def deleteUser(self, user_id: ObjectId):
        return self.collection.delete_one({"_id": user_id})


user_repository = __UserRepository()
