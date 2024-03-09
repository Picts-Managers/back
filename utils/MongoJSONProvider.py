import logging
from flask.json.provider import DefaultJSONProvider
from bson import ObjectId
from pydantic import BaseModel


class MongoJSONProvider(DefaultJSONProvider):
    def __init__(self, app):
        super().__init__(app)

    def default(self, o):
        if issubclass(type(o), BaseModel):
            return o.model_dump()
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(self, o)
