from pydantic import BaseModel, Field

from utils.regex import isEmail, isUsername


class Request(BaseModel):
    username: str = Field(default=None, pattern=isUsername)
    email: str = Field(default=None, pattern=isEmail)


class Response(BaseModel):
    username: str
    email: str
    id: str
