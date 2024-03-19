from pydantic import BaseModel, Field

from utils.regex import isObjectId


class Request(BaseModel):
    picture_id: str = Field(pattern=isObjectId)
