from types import ModuleType
from typing import Any

from bson import ObjectId
from flask.wrappers import Request as FlaskRequest
from pydantic import BaseModel, ConfigDict, Field
from pydantic_core import PydanticUndefined


class ParsedRequest(FlaskRequest):
    def __init__(self, query=None, body=None):
        self.query = query
        self.body = body


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


_Unset: Any = PydanticUndefined


class DbObject(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    id: ObjectId = Field(default=None, alias="_id")

    def model_dump(self, by_alias=True, exclude_none=True):
        return super().model_dump(by_alias=by_alias, exclude_none=exclude_none)
