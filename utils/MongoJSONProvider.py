from bson import ObjectId
from flask.json.provider import DefaultJSONProvider
from pydantic import BaseModel


class MongoJSONProvider(DefaultJSONProvider):
    def __init__(self, app):
        super().__init__(app)

    def default(self, o):
        if issubclass(type(o), BaseModel):
            return dict(o)
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(self, o)
