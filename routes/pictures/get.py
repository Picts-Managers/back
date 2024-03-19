from bson import ObjectId
from flask import abort, request, send_file

from middlewares import schema
from middlewares.auth import isLogged
from repositories import picture_repository
from schemas.pictures import getPictures
from utils import route


@route("/")
@isLogged
@schema(getPictures)
def get_pictures():
    pictures = picture_repository.getMyPictures(request.req_user.id)
    pictures.sort(key=lambda x: x.date, reverse=False)
    return {"pictures": pictures}


@route("/<picture_id>")
@isLogged
def get_specific_picture_file(picture_id: str):
    _picture_id = ObjectId(picture_id)
    picture = picture_repository.getPicture(_picture_id)
    if not picture:
        abort(404, description="Picture not found")
    return send_file(f"../uploads/{picture.id}", mimetype=picture.mimetype)


@route("/<picture_id>/low")
@isLogged
def get_specific_picture_file_low_res(picture_id: str):
    _picture_id = ObjectId(picture_id)
    picture = picture_repository.getPicture(_picture_id)
    if not picture:
        abort(404, description="Picture not found")
    return send_file(f"../uploads/{picture.id}.low", mimetype=picture.mimetype)
