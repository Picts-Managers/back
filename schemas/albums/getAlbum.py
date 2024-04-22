from typing import Optional

from pydantic import BaseModel


class Response(BaseModel):
    id: str
    owner_id: str
    cover_id: Optional[str] = None
    title: str
    viewers_ids: list[str] = []
    pictures_ids: list[str] = []
