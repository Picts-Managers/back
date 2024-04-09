from bson import ObjectId
from flask import request

from middlewares import schema
from middlewares.auth import isLogged
from repositories import picture_repository, user_repository
from schemas.pictures import sharePicture
from utils.routeDecorator import route


@route("/<picture_id>/share")
@isLogged
@schema(sharePicture)
def share_picture(picture_id):
    target_user_email = request.body.email
    target_user = user_repository.getUserByEmail(target_user_email)

    picture_id = ObjectId(picture_id)
    picture = picture_repository.share(picture_id, target_user.id)
    return picture
