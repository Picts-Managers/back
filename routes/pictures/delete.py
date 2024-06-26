from bson import ObjectId
from flask import Blueprint, abort, request

from middlewares.auth import isLogged
from repositories import picture_repository

blueprint = Blueprint(__name__.replace(".", "/"), __name__)


@blueprint.delete("/<picture_id>")
@isLogged
def delete_picture(picture_id: str):
    if not ObjectId.is_valid(picture_id):
        abort(400, "Invalid picture id")
    picture = picture_repository.getPicture(ObjectId(picture_id))
    if not picture:
        abort(404, "Album not found")
    if request.req_user.id != picture.owner_id:
        abort(403, "You must be the owner of the picture to delete it")
    picture_repository.deletePicture(picture.id)

    return {"message": "deleted"}
