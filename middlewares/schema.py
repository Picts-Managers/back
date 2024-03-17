
from functools import wraps
from flask import abort, request
import logging

from pydantic import BaseModel
from utils.types import Schema as SchemaType

__logger = logging.getLogger(__name__)


def schema(schema: SchemaType):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if hasattr(schema, "Query") and issubclass(schema.Query, BaseModel):
                try:
                    query = schema.Query(**dict(request.args))
                except:
                    return abort(400, "Invalid query parameters")
            else:
                query = None

            if hasattr(schema, "Request") and issubclass(schema.Request, BaseModel):
                try:
                    body = schema.Request(request.json)
                except:
                    return abort(400, "Invalid request body")
            else:
                body = None

            request.body = body
            request.query = query
            res =  func(*args, **kwargs)
            if  hasattr(schema, "Response") and issubclass(schema.Response, BaseModel):
                try:
                    response = schema.Response()
                except:
                    return abort(500, "Invalid response schema")
            return res

        return wrapper
    return decorator