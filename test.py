from bson import ObjectId
from pydantic import BaseModel, ConfigDict

from utils.types import DbObject, Field


class User(DbObject):
    username: str
    password: str = None
    email: str


# Example usage
if __name__ == "__main__":
    obj = User(id=ObjectId(), username="test", email="a@example.com", password="1234")
    print(obj)
    print(obj.id)
