from pydantic import BaseModel, Field

from utils.regex import isJWT


class Request(BaseModel):
    login: str
    password: str


class Response(BaseModel):
    access_token: str = Field(pattern=isJWT)
