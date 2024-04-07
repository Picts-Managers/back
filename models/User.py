from utils.types import DbObject


class User(DbObject):
    username: str
    password: str = None
    email: str
