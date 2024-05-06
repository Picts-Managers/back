from pydantic import BaseModel

from utils.types import ResAlbum


class Response(BaseModel):
    albums: list[ResAlbum] = []
