from bson import ObjectId
from flask import Blueprint, abort, request

from middlewares import schema
from middlewares.auth import isLogged
from repositories import album_repository, picture_repository, user_repository
from schemas.albums import addPictureToAlbum, shareAlbum
from utils.image import handle_picture_upload

blueprint = Blueprint(__name__.replace(".", "/"), __name__)


@blueprint.patch("/<album_id>")
@isLogged
@schema(addPictureToAlbum)
def add_picture_in_album(album_id: str):

    if not ObjectId.is_valid(album_id):
        abort(400, "Invalid album id")

    album_id = ObjectId(album_id)
    picture_id = ObjectId(request.body.picture_id)

    target_album = album_repository.getAlbum(album_id)
    if not target_album:
        abort(404, "Album not found")
    if picture_id in target_album.pictures_ids:
        abort(400, "Picture already in album")

    if picture_repository.getPicture(picture_id):
        album = album_repository.addPicture(
            album_id,
            picture_id,
        )
    else:
        abort(404, "Picture not found")

    return album


@blueprint.patch("/upload/<album_id>")
@isLogged
def upload_picture_to_album(album_id: str):
    uploaded_file = request.files["file"]
    picture = handle_picture_upload(uploaded_file)

    album_id = ObjectId(album_id)
    album = album_repository.addPicture(
        album_id,
        picture.id,
    )
    return album


@blueprint.patch("/<album_id>/share")
@isLogged
@schema(shareAlbum)
def share_album(album_id):
    if not ObjectId.is_valid(album_id) or not request.body:
        abort(400, "Invalid picture id")

    target_user = user_repository.getUserByEmail(request.body.email)
    if not target_user:
        abort(404, "User not found")

    album_id = ObjectId(album_id)
    album = album_repository.getAlbum(album_id)
    if not album:
        abort(404, "Album not found")

    if target_user.id in album.viewers_ids:
        abort(400, "Album already shared with this user")

    album = album_repository.share(album_id, target_user.id)
    return album
