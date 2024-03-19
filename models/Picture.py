from datetime import datetime

from bson import ObjectId

from utils.types import DbObject, Field


class Picture(DbObject):
    owner_id: ObjectId = Field(default=None, alias="_owner_id")
    filename: str
    date: str = Field(default=datetime.now().isoformat())
    location: dict = Field(default=None)
    viewers_ids: list[ObjectId] = Field(default=[])
    mimetype: str = Field(default=None)
