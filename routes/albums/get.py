from bson import ObjectId
from flask import abort, request, send_file

from middlewares import isLogged, schema
from repositories import album_repository, picture_repository
from schemas.albums import getAlbum, getAlbums
from utils import route


@route("/")
@isLogged
@schema(getAlbums)
def get_albums():
    albums = album_repository.getMyAlbums(request.req_user.id)
    for album in albums:
        album.cover_id = album.pictures_ids[0] if len(album.pictures_ids) else None
    return {"albums": albums}


@route("/<album_id>")
@isLogged
@schema(getAlbum)
def get_album(album_id: str):
    if not ObjectId.is_valid(album_id):
        abort(400, "Invalid album id")
    album = album_repository.getAlbum(ObjectId(album_id))
    if not album:
        abort(404, "Album not found")
    if (
        request.req_user.id not in album.viewers_ids
        and request.req_user.id != album.owner_id
    ):
        abort(403, "You don't have access to this album")

    album.cover_id = album.pictures_ids[0] if len(album.pictures_ids) else None
    return album


@route("/shared")
@isLogged
def get_shared_albums(request):
    albums = album_repository.getSharedAlbums(request.req_user.id)
    for album in albums:
        album.cover_id = album.pictures_ids[0] if len(album.pictures_ids) else None
    return {"albums": albums}


@route("/<album_id>/<picture_id>")
@isLogged
def get_picture_in_album(album_id: str, picture_id: str):
    album_id = ObjectId(album_id)
    picture_id = ObjectId(picture_id)

    album = album_repository.getAlbum(album_id)
    if not album:
        abort(404, "Album not found")
    if picture_id not in album.pictures_ids:
        abort(404, "Picture not found in album")
    if (
        request.req_user.id not in album.viewers_ids
        and request.req_user.id != album.owner_id
    ):
        abort(403, "You don't have access to this album")
    picture = picture_repository.getPicture(picture_id)
    if not picture:
        abort(404, "Picture not found")
    return send_file(f"../uploads/{picture.id}", mimetype=picture.mimetype)


@route("/<album_id>/<picture_id>/low")
@isLogged
def get_picture_in_album_low_res(album_id: str, picture_id: str):
    album_id = ObjectId(album_id)
    picture_id = ObjectId(picture_id)

    album = album_repository.getAlbum(album_id)
    if not album:
        abort(404, "Album not found")
    if picture_id not in album.pictures_ids:
        abort(404, "Picture not found in album")
    if (
        request.req_user.id not in album.viewers_ids
        and request.req_user.id != album.owner_id
    ):
        abort(403, "You don't have access to this album")
    picture = picture_repository.getPicture(picture_id)
    if not picture:
        abort(404, "Picture not found")
    return send_file(f"../uploads/{picture.id}.low", mimetype=picture.mimetype)
