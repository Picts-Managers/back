from flask import request

from middlewares import schema
from middlewares.auth import isLogged
from models import Album
from repositories import album_repository
from schemas.albums import createAlbum
from utils import route


@route("/")
@isLogged
@schema(createAlbum)
def create_album():
    album_name = request.body.name
    album = Album(
        owner_id=request.req_user.id,
        title=album_name,
    )
    album = album_repository.insertAlbum(album)
    return album
