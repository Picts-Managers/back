from pydantic import BaseModel, Field

from utils.regex import isEmail, isUsername


class Request(BaseModel):
    username: str = Field(pattern=isUsername)
    email: str = Field(pattern=isEmail)


class Response(BaseModel):
    username: str
    email: str
    id: str
