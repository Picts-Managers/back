from bson import ObjectId
from pydantic import BaseModel, Field


class Account(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: ObjectId = Field(default=None, alias="_id")
    user_id: ObjectId = Field(default=None, alias="_user_id")
    name: str = None
    puuid: str = None
    tag: str = None
    account_id: str = None
    tier: int = None
    rank: int = None
    lp: int = None

    def model_dump(self):
        return super().model_dump(by_alias=True, exclude_unset=True)
