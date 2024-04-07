from bson import ObjectId
from flask import request

from middlewares import schema
from middlewares.auth import isLogged
from repositories import picture_repository
from schemas.pictures import sharePicture
from utils.routeDecorator import route


@route("/share/<picture_id>")
@isLogged
@schema(sharePicture)
def share_picture(picture_id):
    target_user_id = ObjectId(request.body.user)
    picture_id = ObjectId(picture_id)
    picture = picture_repository.share(picture_id, target_user_id)
    return picture
