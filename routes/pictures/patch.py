from bson import ObjectId
from flask import abort, request

from middlewares import schema
from middlewares.auth import isLogged
from repositories import picture_repository, user_repository
from schemas.pictures import sharePicture
from utils.routeDecorator import route


@route("/<picture_id>/share")
@isLogged
@schema(sharePicture)
def share_picture(picture_id: str):
    if not ObjectId.is_valid(picture_id):
        abort(400, "Invalid picture id")

    target_user = user_repository.getUserByEmail(request.body.email)
    if not target_user:
        abort(404, "User not found")

    picture_id = ObjectId(picture_id)
    picture = picture_repository.sharePicture(picture_id, target_user.id)
    return picture
