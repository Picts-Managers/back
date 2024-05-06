from datetime import datetime

from bson import ObjectId
from flask import Blueprint, abort, request
from PIL import Image

from middlewares import schema
from middlewares.auth import isLogged
from models import Picture
from repositories import album_repository, picture_repository
from schemas.albums import addPictureToAlbum, shareAlbum
from utils.image import get_metadata

blueprint = Blueprint(__name__.replace(".", "/"), __name__)


@blueprint.patch("/<album_id>")
@isLogged
@schema(addPictureToAlbum)
def add_picture_in_album(album_id: str):

    if not ObjectId.is_valid(album_id):
        abort(400, "Invalid album id")
    if not ObjectId.is_valid(request.body.picture_id):
        abort(400, "Invalid picture id")

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
    image = Image.open(uploaded_file)
    filename = ".".join(uploaded_file.filename.split(".")[:-1])
    metadata = get_metadata(image)
    picture = Picture(
        owner_id=request.req_user.id,
        location=metadata.get("location", None),
        date=metadata.get("date", datetime.now().isoformat()),
        filename=filename,
        mimetype=uploaded_file.mimetype,
    )
    picture = picture_repository.insertPicture(picture)

    if image.mode == "RGBA" or image.mode == "P":
        if image.mode == "P":
            image = image.convert("RGBA")

        white_image = Image.new("RGBA", image.size, "WHITE")
        white_image.paste(image, mask=image)
        image = white_image.convert("RGB")

    image.save(f"uploads/{picture.id}", "JPEG")
    image.thumbnail((200, 200))
    image.save(f"uploads/{picture.id}.low", "JPEG")

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
    target_user_id = ObjectId(request.body.user)
    album_id = ObjectId(album_id)
    album = album_repository.share(album_id, target_user_id)
    return album
