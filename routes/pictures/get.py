from bson import ObjectId
from flask import abort

from repositories import picture_repository
from utils import route


@route("/")
def index():
    pictures = picture_repository.getPictures()
    return pictures


@route("/<picture_id>")
def index(picture_id: str):
    _picture_id = ObjectId(picture_id)
    picture = picture_repository.getPicture(_picture_id)
    if not len(picture):
        abort(404, description="Picture not found")
    picture = picture[0]
    return picture
