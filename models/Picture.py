from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime


class Picture(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: ObjectId = Field(default=None, alias="_id")
    owner_id: ObjectId = Field(default=None, alias="_owner_id")
    filename: str = None
    date: str = Field(default=datetime.now().isoformat())
    location: dict = None
    viewers_ids: list[ObjectId] = Field(default=[])
    mimetype: str = None

    def model_dump(self):
        return super().model_dump(by_alias=True, exclude_unset=True)
