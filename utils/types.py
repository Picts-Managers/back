from types import ModuleType

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


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
