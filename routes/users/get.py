from bson import ObjectId

from repositories import user_repository


def index(user_id: str):
    _user_id = ObjectId(user_id)
    user = user_repository.getUser(_user_id)
    if not len(user) or len(user) > 1:
        return "error"
    user = user[0]
    return user.model_dump()