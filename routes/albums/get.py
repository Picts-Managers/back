from middlewares.auth import isLogged
from repositories import album_repository
from utils import route


@route("/")
@isLogged
def get_albums():
    albums = album_repository.getAlbums()
    for album in albums:
        album.cover_id = album.pictures_ids[0] if len(album.pictures_ids) else None
    return albums
