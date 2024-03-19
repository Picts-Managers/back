from typing import Optional

from pydantic import BaseModel, Field

from utils.regex import isValidName


class Request(BaseModel):
    name: str = Field(pattern=isValidName)


class Response(BaseModel):
    id: str
    owner_id: str
    title: str
    cover_id: Optional[str] = None
    viewers_ids: list[str] = []
    pictures_ids: list[str] = []
