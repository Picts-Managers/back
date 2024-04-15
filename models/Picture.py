from typing import Optional

from bson import ObjectId

from utils.types import Coordinates, DbObject, Field


class Picture(DbObject):
    owner_id: ObjectId = Field(default=None, alias="_owner_id")
    filename: str
    date: str
    location: Optional[Coordinates] = None
    viewers_ids: list[ObjectId] = []
    mimetype: str
    is_fav: bool = False
