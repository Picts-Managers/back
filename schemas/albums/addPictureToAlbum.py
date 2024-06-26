from typing import Optional
from pydantic import BaseModel, Field

from utils.regex import isObjectId


class Request(BaseModel):
    picture_id: str = Field(pattern=isObjectId)


class Response(BaseModel):
    id: str
    owner_id: str
    title: str
    cover_id: Optional[str] = None
    viewers_ids: list[str] = []
    pictures_ids: list[str] = []
