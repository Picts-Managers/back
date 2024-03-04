from bson import ObjectId
from utils.db import client
import os
from models.Account import Account


class __AccountRepository:
    def __init__(self):
        self.collection = client[os.getenv("DB_NAME")].accounts

    def getUserAccounts(self, user_id: ObjectId) -> list[Account]:
        return [
            Account(**account)
            for account in self.collection.find({"_user_id": user_id})
            if account is not None
        ]

    def getUserMainAccount(self, user_id: ObjectId) -> Account | None:
        result = list(
            self.collection.aggregate(
                [
                    {"$match": {"_user_id": user_id}},
                    {"$sort": {"tier": -1, "rank": 1, "lp": -1}},
                    {"$limit": 1},
                ]
            )
        )
        if len(result):
            return Account(**result[0])
        return None

    def insertAccount(self, new_account: Account):
        return self.collection.insert_one(new_account.model_dump())

    def updateAccount(self, account_id: ObjectId, new_account: Account):
        return self.collection.update_one(
            {"_id": account_id}, {"$set": new_account.model_dump()}
        )

    def deleteAccount(self, account_id: ObjectId):
        return self.collection.delete_one({"_id": account_id})


account_repository = __AccountRepository()
