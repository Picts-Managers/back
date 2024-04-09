from typing import Optional

from pydantic import BaseModel


class Response(BaseModel):
    id: str
    owner_id: str
    title: str
    cover_id: Optional[str] = None
    viewers_ids: list[str] = []
    pictures_ids: list[str] = []
