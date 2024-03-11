from datetime import datetime
from bson import ObjectId
from flask import abort, request
from models import Picture

from repositories import album_repository, picture_repository
from utils import route
from PIL import Image

from utils.image import get_metadata


@route("/<album_id>")
def index(album_id: str):
    uploaded_file = request.files["file"]
    image = Image.open(uploaded_file)
    filename = ".".join(uploaded_file.filename.split(".")[:-1])
    metadata = get_metadata(image)
    picture = Picture(
        id=ObjectId(),
        owner_id=ObjectId("65e73cb103d93e117cadf9a9"),
        date=metadata.get("date", datetime.now().isoformat()),
        filename=filename,
        mimetype=uploaded_file.mimetype,
    )
    if metadata.get("location"):
        picture.location = metadata["location"]
    picture = picture_repository.insertPicture(picture)

    image.convert("RGB").save(f"uploads/{picture.id}", "JPEG")

    album_id = ObjectId(album_id)
    album = album_repository.addPicture(
        album_id,
        picture.id,
    )
    return {"album": album, "picture": picture}


@route("/<album_id>/<picture_id>")
def index(album_id: str, picture_id: str):
    album_id = ObjectId(album_id)
    picture_id = ObjectId(picture_id)
    album = album_repository.addPicture(
        album_id,
        picture_id,
    )
    return album
