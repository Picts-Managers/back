from bson import ObjectId
from flask import abort

from repositories import album_repository
from utils import route


@route("/")
def index():
    albums = album_repository.getAlbums()
    for album in albums:
        album.cover_id = album.pictures_ids[0] if len(album.pictures_ids) else None
    return albums


@route("/<album_id>")
def index(album_id: str):
    _album_id = ObjectId(album_id)
    album = album_repository.getAlbum(_album_id)
    if not len(album):
        abort(404, description="Album not found")
    album = album[0]
    return album
