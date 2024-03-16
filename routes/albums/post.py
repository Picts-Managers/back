from bson import ObjectId
from flask import abort, request
from models import Album

from repositories import album_repository
from utils import route


@route("/")
def create_album():
    album_name = request.json.get("name")

    album = Album(
        owner_id=ObjectId("65e73cb103d93e117cadf9a9"),
        title=album_name,
    )
    album = album_repository.insertAlbum(album)
    return album
