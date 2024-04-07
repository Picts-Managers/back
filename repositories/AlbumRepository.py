import os

from bson import ObjectId

from models import Album
from utils.db import client


class __AlbumRepository:
    def __init__(self):
        self.collection = client[os.getenv("DB_NAME")].albums

    def getAlbums(self) -> list[Album]:
        return [
            Album(**album) for album in self.collection.find({}) if album is not None
        ]

    def getMyAlbums(self, owner_id: ObjectId) -> list[Album]:
        return [
            Album(**album)
            for album in self.collection.find({"_owner_id": owner_id})
            if album is not None
        ]

    def getAlbum(self, album_id: ObjectId) -> Album:
        album = self.collection.find_one({"_id": album_id})
        return Album(**album) if album else None

    def getSharedAlbums(self, user_id: ObjectId) -> list[Album]:
        return [
            Album(**album)
            for album in self.collection.find({"viewers_ids": user_id})
            if album is not None
        ]

    def insertAlbum(self, new_album: Album):
        result = self.collection.insert_one(new_album.model_dump())
        inserted_album = self.collection.find_one({"_id": result.inserted_id})
        return Album(**inserted_album) if inserted_album else None

    def addPicture(self, album_id: ObjectId, picture_id: ObjectId):
        self.collection.update_one(
            {"_id": album_id}, {"$push": {"pictures_ids": picture_id}}
        )
        updated_album = self.collection.find_one({"_id": album_id})
        return Album(**updated_album) if updated_album else None

    def share(self, album_id: ObjectId, user_id: ObjectId):
        self.collection.update_one(
            {"_id": album_id}, {"$push": {"viewers_ids": user_id}}
        )
        updated_album = self.collection.find_one({"_id": album_id})
        return Album(**updated_album) if updated_album else None

    def updateAlbum(self, album_id: ObjectId, new_album: Album):
        self.collection.update_one({"_id": album_id}, {"$set": new_album.model_dump()})
        updated_album = self.collection.find_one({"_id": album_id})
        return Album(**updated_album) if updated_album else None

    def deleteAlbum(self, album_id: ObjectId):
        return self.collection.delete_one({"_id": album_id})


album_repository = __AlbumRepository()
