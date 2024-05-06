import datetime
from types import ModuleType
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator


class QueryType(BaseModel):
    pass


class RequestType(BaseModel):
    pass


class ResponseType(BaseModel):
    pass


class Schema(ModuleType):
    Query: QueryType
    Request: RequestType
    Response: ResponseType


class ObjectFromDict:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class DbObject(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="allow",
    )

    id: ObjectId = Field(default=None, alias="_id")

    def model_dump(self, by_alias=True, exclude_none=True):
        return super().model_dump(by_alias=by_alias, exclude_none=exclude_none)


class Coordinates(BaseModel):
    latitude: str
    longitude: str


class ResPicture(BaseModel):
    id: str
    filename: str
    owner_id: str
    date: str = None
    is_fav: bool = False
    location: Optional[Coordinates] = None
    viewers_ids: list[str] = []

    @field_validator("date")
    def validate_date(cls, value):
        if value is None:
            return ObjectId(cls.id).generation_time.isoformat()
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        return value


class ResAlbum(BaseModel):
    id: str
    owner_id: str
    cover_id: Optional[str] = None
    title: str
    viewers_ids: list[str] = []
    pictures: list[ResPicture] = []
