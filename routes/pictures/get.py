from bson import ObjectId
from flask import abort, send_file

from middlewares.auth import isLogged
from repositories import picture_repository
from utils import route


@route("/")
@isLogged
def get_pictures():
    pictures = picture_repository.getPictures()
    pictures.sort(key=lambda x: x.date, reverse=False)
    return pictures


@route("/<picture_id>")
@isLogged
def get_specific_picture_file(picture_id: str):
    _picture_id = ObjectId(picture_id)
    picture = picture_repository.getPicture(_picture_id)
    if not len(picture):
        abort(404, description="Picture not found")
    picture = picture[0]
    return send_file(f"../uploads/{picture.id}", mimetype=picture.mimetype)
