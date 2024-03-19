import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, field_validator


class _ResLocation(BaseModel):
    latitude: str
    longitude: str


class Response(BaseModel):
    id: str
    filename: str
    owner_id: str
    date: Optional[str] = None
    location: Optional[_ResLocation] = None
    viewers_ids: Optional[list[str]] = []

    @field_validator("date")
    def validate_date(cls, value):
        if value is None:
            return ObjectId(cls.id).generation_time.isoformat()
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        return value
