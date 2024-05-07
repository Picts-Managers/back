import logging
import os
from functools import wraps

from flask import abort, json, request
from pydantic import BaseModel, ValidationError

from utils.types import Schema as SchemaType

__logger = logging.getLogger(__name__)

IS_DEBUG = os.getenv("ENV") != "production"


def schema(schema: SchemaType):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if hasattr(schema, "Query") and issubclass(schema.Query, BaseModel):
                try:
                    request.query = schema.Query(**dict(request.args))
                except ValidationError as e:
                    return abort(400, "Bad Request" + f": {e}" if IS_DEBUG else "")

            if (
                hasattr(schema, "Request")
                and issubclass(schema.Request, BaseModel)
                and request.headers.get("content-type") == "application/json"
            ):
                try:
                    request.body = schema.Request(**request.json)
                except ValidationError as e:
                    return abort(400, "Bad Request" + f": {e}" if IS_DEBUG else "")

            res = func(*args, **kwargs)

            if hasattr(schema, "Response") and issubclass(schema.Response, BaseModel):
                try:
                    prepared_res = json.loads(json.dumps(res))
                    response = schema.Response(**dict(prepared_res))
                    return response
                except ValidationError as e:
                    return abort(
                        500, "Invalid response schema" + f": {e}" if IS_DEBUG else ""
                    )
            return res

        return wrapper

    return decorator
