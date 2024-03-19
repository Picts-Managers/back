from typing import Optional

from pydantic import BaseModel, Field


class _ResAlbum(BaseModel):
    owner_id: str
    cover_id: Optional[str] = None
    title: str
    viewers_ids: list[str] = []
    pictures_ids: list[str] = []


class Response(BaseModel):
    albums: list[_ResAlbum] = []
