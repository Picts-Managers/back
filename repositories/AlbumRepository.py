from bson import ObjectId
from utils.db import client
import os
from models import Album


class __AlbumRepository:
    def __init__(self):
        self.collection = client[os.getenv("DB_NAME")].albums

    def getAlbums(self) -> list[Album]:
        return [
            Album(**album) for album in self.collection.find({}) if album is not None
        ]

    def getAlbum(self, album_id: ObjectId) -> list[Album]:
        return [
            Album(**album)
            for album in self.collection.find({"_id": album_id})
            if album is not None
        ]

    def insertAlbum(self, new_album: Album):
        result = self.collection.insert_one(new_album.model_dump())
        inserted_album = self.collection.find_one({"_id": result.inserted_id})
        return Album(**inserted_album) if inserted_album else None

    def updateAlbum(self, album_id: ObjectId, new_album: Album):
        self.collection.update_one({"_id": album_id}, {"$set": new_album.model_dump()})
        updated_album = self.collection.find_one({"_id": album_id})
        return Album(**updated_album) if updated_album else None

    def deleteAlbum(self, album_id: ObjectId):
        return self.collection.delete_one({"_id": album_id})


album_repository = __AlbumRepository()
