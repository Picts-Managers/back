from pydantic import BaseModel

from utils.types import ResPicture


class Response(BaseModel):
    pictures: list[ResPicture] = []
