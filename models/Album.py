from bson import ObjectId

from utils.types import DbObject, Field


class Album(DbObject):
    owner_id: ObjectId = Field(default=None, alias="_owner_id")
    cover_id: ObjectId = Field(default=None, alias="_cover_id")
    title: str
    viewers_ids: list[ObjectId] = Field(default=[])
    pictures_ids: list[ObjectId] = Field(default=[])
