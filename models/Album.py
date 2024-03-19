from typing import Optional

from bson import ObjectId

from utils.types import DbObject, Field


class Album(DbObject):
    owner_id: ObjectId = Field(default=None, alias="_owner_id")
    title: str
    viewers_ids: list[ObjectId] = []
    pictures_ids: list[ObjectId] = []
