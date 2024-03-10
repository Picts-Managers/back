from bson import ObjectId
from utils.db import client
import os
from models import Picture


class __PictureRepository:
    def __init__(self):
        self.collection = client[os.getenv("DB_NAME")].pictures

    def getPictures(self) -> list[Picture]:
        return [
            Picture(**picture)
            for picture in self.collection.find({})
            if picture is not None
        ]

    def getPicture(self, picture_id: ObjectId) -> list[Picture]:
        return [
            Picture(**picture)
            for picture in self.collection.find({"_id": picture_id})
            if picture is not None
        ]

    def insertPicture(self, new_picture: Picture):
        result = self.collection.insert_one(new_picture.model_dump())
        inserted_picture = self.collection.find_one({"_id": result.inserted_id})
        return Picture(**inserted_picture) if inserted_picture else None

    def updatePicture(self, picture_id: ObjectId, new_picture: Picture):
        self.collection.update_one(
            {"_id": picture_id}, {"$set": new_picture.model_dump()}
        )
        updated_picture = self.collection.find_one({"_id": picture_id})
        return Picture(**updated_picture) if updated_picture else None

    def deletePicture(self, picture_id: ObjectId):
        return self.collection.delete_one({"_id": picture_id})


picture_repository = __PictureRepository()