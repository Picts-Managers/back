from pydantic import BaseModel, Field

from utils.regex import isEmail


class Request(BaseModel):
    email: str = Field(pattern=isEmail)
