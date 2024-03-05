from bson import ObjectId
from pydantic import BaseModel, Field


class User(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: ObjectId = Field(default=None, alias="_id")
    username: str = None
    password: str = None
    email: str = None
    token: str = None

    def model_dump(self):
        print(super())
        return super().model_dump_json(by_alias=True, exclude_unset=True)
