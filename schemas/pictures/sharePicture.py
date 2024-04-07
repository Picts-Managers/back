from pydantic import BaseModel, Field

from utils.regex import isObjectId


class Request(BaseModel):
    user: str = Field(pattern=isObjectId)
