from types import ModuleType
from pydantic import BaseModel
from flask.wrappers import Request as FlaskRequest


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