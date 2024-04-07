import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, field_validator

from utils.types import Coordinates


class _ResPictures(BaseModel):
    id: str
    filename: str
    owner_id: str
    date: str = None
    location: Optional[Coordinates] = None
    viewers_ids: list[str] = []

    @field_validator("date")
    def validate_date(cls, value):
        if value is None:
            return ObjectId(cls.id).generation_time.isoformat()
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        return value


class Response(BaseModel):
    pictures: list[_ResPictures] = []
