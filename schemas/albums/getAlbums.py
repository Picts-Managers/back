from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class _ResAlbum(BaseModel):
    owner_id: str
    cover_id: Optional[str] = Field(default=None)
    title: str
    viewers_ids: Optional[list[str]] = Field(default=[])
    pictures_ids: Optional[list[str]] = Field(default=[])


class Response(BaseModel):
    albums: list[_ResAlbum] = Field(default=[])
