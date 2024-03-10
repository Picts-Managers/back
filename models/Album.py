from bson import ObjectId
from pydantic import BaseModel, Field


class Album(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: ObjectId = Field(default=None, alias="_id")
    owner_id: ObjectId = Field(default=None, alias="_owner_id")
    title: str
    viewers_ids: list[ObjectId] = []
    pictures_ids: list[ObjectId] = []

    def model_dump(self):
        return super().model_dump(by_alias=True, exclude_unset=True)
