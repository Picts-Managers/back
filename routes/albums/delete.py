from bson import ObjectId
from flask import abort, request

from middlewares.auth import isLogged
from repositories import album_repository
from utils.routeDecorator import route


@route("/<album_id>")
@isLogged
def get_album(album_id: str):
    if not ObjectId.is_valid(album_id):
        abort(400, "Invalid album id")
    album = album_repository.getAlbum(ObjectId(album_id))
    if not album:
        abort(404, "Album not found")
    if request.req_user.id != album.owner_id:
        abort(403, "You must be the owner of the album to delete it")
    album_repository.deleteAlbum(album.id)

    return {"message": "deleted"}
