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
    response = []
    for album in albums:
        tmp = dict(album)
        tmp["cover_ide"] = album.pictures_ids[0] if len(album.pictures_ids) else None
        response.append(tmp)
    return {"albums": response}
