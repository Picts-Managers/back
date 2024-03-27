from flask import request

from middlewares import isLogged, schema
from repositories import album_repository
from schemas.albums import getAlbums
from utils import route


@route("/")
@isLogged
@schema(getAlbums)
def get_albums():
    albums = album_repository.getMyAlbums(request.req_user.id)
    for album in albums:
        album.cover_id = album.pictures_ids[0] if len(album.pictures_ids) else None
    return {"albums": albums}
