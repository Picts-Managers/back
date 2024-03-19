from utils.types import DbObject, Field


class User(DbObject):
    username: str
    password: str = Field(default=None)
    email: str
