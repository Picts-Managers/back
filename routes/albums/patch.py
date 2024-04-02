from datetime import datetime

from bson import ObjectId
from flask import abort, request
from PIL import Image

from middlewares import schema
from middlewares.auth import isLogged
from models import Picture
from repositories import album_repository, picture_repository
from schemas.albums import addPictureToAlbum
from utils import route
from utils.image import get_metadata


@route("/<album_id>")
@isLogged
@schema(addPictureToAlbum)
def add_picture_in_album(album_id: str):
    not_found_error = False

    pictures = request.body.picture_id
    album_id = ObjectId(album_id)
    for picture in pictures:
        picture_id = ObjectId(picture)
        if picture_repository.getPicture(picture_id):
            album = album_repository.addPicture(
                album_id,
                picture_id,
            )
        else:
            not_found_error = True
            continue
    if not_found_error:
        abort(404, "Some picture not found")
    return album


@route("/upload/<album_id>")
@isLogged
@schema(addPictureToAlbum)
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

    if uploaded_file.mimetype == "image/png":
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
    return {"album": album, "picture": picture}


@route("/share/<album_id>")
@isLogged
def share_album(album_id):
    target_user_id = ObjectId(request.body.user)
    album_id = ObjectId(album_id)
    album = album_repository.share(album_id, target_user_id)
    return album
