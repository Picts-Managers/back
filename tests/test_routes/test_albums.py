import io
import shutil

import pytest
from bson import ObjectId
from PIL import Image

from utils import app, auth, db

token = None


@pytest.fixture(autouse=True, scope="module")
def get_token():
    global token

    token = auth.generate_token(ObjectId("663a200fcb14e84e2fff0db8"))
    yield
    token = None


def test_create_album_success():
    response = app.test_client().post(
        "/albums/",
        headers={
            "Authorization": "Bearer " + token,
        },
        json={
            "name": "test_album",
        },
    )

    assert response.status_code == 200

    assert "id" in response.json
    assert response.json.get("title") == "test_album"
    assert response.json.get("cover_id") is None
    assert response.json.get("owner_id") == "663a200fcb14e84e2fff0db8"
    assert response.json.get("viewers_ids") == []
    assert response.json.get("pictures") == []


def test_get_albums_success():
    response = app.test_client().get(
        "/albums/",
        headers={
            "Authorization": "Bearer " + token,
        },
    )
    assert response.status_code == 200

    assert isinstance(response.json.get("albums"), list)
    assert len(response.json.get("albums", [])) == 1
    assert response.json.get("albums", [])[0].get("title") == "test_album"


def test_get_album_success():
    album = db.client.albums.find_one(
        {"_owner_id": ObjectId("663a200fcb14e84e2fff0db8")}
    )
    response = app.test_client().get(
        f"/albums/{album.get('_id')}",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 200

    assert response.json.get("title") == "test_album"


def test_get_album_invalid_id():
    response = app.test_client().get(
        "/albums/1",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 400


def test_get_album_not_found():
    response = app.test_client().get(
        f"/albums/{'0' * 24}",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 404


def test_get_album_no_rights():
    album = db.client.albums.insert_one(
        {
            "_owner_id": ObjectId("0" * 24),
            "title": "test_album_fake_user",
            "viewers_ids": [],
            "pictures_ids": [],
        }
    )

    response = app.test_client().get(
        f"/albums/{album.inserted_id}",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 403


def test_add_image_to_album():
    image_path = "./tests/assets/pictures/background_luffy.png"
    album = db.client.albums.find_one(
        {"_owner_id": ObjectId("663a200fcb14e84e2fff0db8")}
    )

    with open(image_path, "rb") as image:
        response = app.test_client().patch(
            f"/albums/upload/{album.get('_id')}",
            headers={
                "Authorization": "Bearer " + token,
                "Content-Type": "multipart/form-data",
            },
            data={
                "file": (image, image_path.split("/")[-1]),
            },
        )
        assert response.status_code == 200

    album = db.client.albums.find_one({"_id": album.get("_id")})
    assert len(album.get("pictures_ids")) == 1


def test_get_albums_with_picture_success():
    response = app.test_client().get(
        "/albums/",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 200

    assert response.json.get("albums")[0].get("title") == "test_album"
    assert response.json.get("albums")[0].get("cover_id") == response.json.get(
        "albums"
    )[0].get("pictures")[0].get("id")
    assert response.json.get("albums")[0].get("owner_id") == "663a200fcb14e84e2fff0db8"
    assert response.json.get("albums")[0].get("viewers_ids") == []
    assert len(response.json.get("albums")[0].get("pictures")) == 1


def test_get_album_with_picture_success():
    album = db.client.albums.find_one(
        {"_owner_id": ObjectId("663a200fcb14e84e2fff0db8")}
    )
    response = app.test_client().get(
        f"/albums/{album.get('_id')}",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 200

    assert response.json.get("title") == "test_album"
    assert response.json.get("cover_id") == response.json.get("pictures")[0].get("id")
    assert response.json.get("owner_id") == "663a200fcb14e84e2fff0db8"
    assert response.json.get("viewers_ids") == []
    assert len(response.json.get("pictures")) == 1


def test_get_shared_albums_empty_success():
    response = app.test_client().get(
        "/albums/shared",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 200

    assert isinstance(response.json.get("albums"), list)
    assert len(response.json.get("albums")) == 0


def test_get_shared_albums_success():
    picture = db.client.pictures.find_one({})

    new_picture = db.client.pictures.insert_one(
        {
            "_owner_id": ObjectId("0" * 24),
            "filename": "test_picture_shared_2",
            "viewers_ids": [],
            "is_fav": False,
            "date": "2021-08-01T00:00:00.000Z",
            "mimetype": "image/png",
        }
    )
    shutil.copy(
        f"./uploads/{picture.get('_id')}", f"./uploads/{new_picture.inserted_id}"
    )
    shutil.copy(
        f"./uploads/{picture.get('_id')}.low",
        f"./uploads/{new_picture.inserted_id}.low",
    )

    db.client.albums.update_one(
        {
            "_owner_id": ObjectId("0" * 24),
        },
        {
            "$set": {
                "viewers_ids": [ObjectId("663a200fcb14e84e2fff0db8")],
                "pictures_ids": [new_picture.inserted_id],
            }
        },
    )

    response = app.test_client().get(
        "/albums/shared",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 200

    assert isinstance(response.json.get("albums"), list)
    assert len(response.json.get("albums")) == 1
    assert response.json.get("albums")[0].get("title") == "test_album_fake_user"
    assert response.json.get("albums")[0].get("cover_id") == str(
        new_picture.inserted_id
    )
    assert response.json.get("albums")[0].get("owner_id") == "0" * 24
    assert response.json.get("albums")[0].get("viewers_ids") == [
        "663a200fcb14e84e2fff0db8"
    ]
    assert len(response.json.get("albums")[0].get("pictures")) == 1
    assert response.json.get("albums")[0].get("pictures")[0].get("id") == str(
        new_picture.inserted_id
    )


def test_get_favorite_album_empty_success():
    response = app.test_client().get(
        "/albums/fav",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 200

    assert response.json.get("title") == "Favourites"
    assert response.json.get("cover_id") is None
    assert response.json.get("owner_id") == "663a200fcb14e84e2fff0db8"
    assert response.json.get("viewers_ids") == []
    assert response.json.get("pictures") == []


def test_get_favorite_album_success():
    db.client.pictures.update_one({}, {"$set": {"is_fav": True}})
    picture = db.client.pictures.find_one({"is_fav": True})

    response = app.test_client().get(
        "/albums/fav",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 200
    assert response.json.get("title") == "Favourites"
    assert response.json.get("cover_id") == str(picture.get("_id"))
    assert response.json.get("owner_id") == "663a200fcb14e84e2fff0db8"
    assert response.json.get("viewers_ids") == []
    assert len(response.json.get("pictures")) == 1
    assert response.json.get("pictures")[0].get("id") == str(picture.get("_id"))


def test_get_low_res_image_from_album_success():
    album = db.client.albums.find_one(
        {"_owner_id": ObjectId("663a200fcb14e84e2fff0db8")}
    )
    picture = db.client.pictures.find_one(
        {"_owner_id": ObjectId("663a200fcb14e84e2fff0db8")}
    )

    response = app.test_client().get(
        f"/albums/{album.get('_id')}/{picture.get('_id')}/low",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 200

    with Image.open(io.BytesIO(response.data)) as image:
        width, height = image.size
        assert width <= 200
        assert height <= 200


def test_get_image_from_shared_album_success():
    album = db.client.albums.find_one({"_owner_id": ObjectId("0" * 24)})
    picture = db.client.pictures.find_one({"_owner_id": ObjectId("0" * 24)})

    response = app.test_client().get(
        f"/albums/{album.get('_id')}/{picture.get('_id')}",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 200
    with open(f"./uploads/{picture.get('_id')}", "rb") as image:
        assert response.data == image.read()


def test_get_low_res_image_from_shared_album_success():
    album = db.client.albums.find_one({"_owner_id": ObjectId("0" * 24)})
    picture = db.client.pictures.find_one({"_owner_id": ObjectId("0" * 24)})

    response = app.test_client().get(
        f"/albums/{album.get('_id')}/{picture.get('_id')}/low",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 200

    with Image.open(io.BytesIO(response.data)) as image:
        width, height = image.size
        assert width <= 200
        assert height <= 200


def test_get_image_album_not_found():
    picture = db.client.pictures.find_one({"_owner_id": ObjectId("0" * 24)})

    response = app.test_client().get(
        f"/albums/{'0' * 24}/{picture.get('_id')}",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 404


def test_get_low_res_image_album_not_found():
    picture = db.client.pictures.find_one({"_owner_id": ObjectId("0" * 24)})

    response = app.test_client().get(
        f"/albums/{'0' * 24}/{picture.get('_id')}/low",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 404


def test_get_image_not_in_album():
    album = db.client.albums.find_one({"_owner_id": ObjectId("0" * 24)})

    response = app.test_client().get(
        f"/albums/{album.get('_id')}/{'0' * 24}",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 404


def test_get_low_res_image_not_in_album():
    album = db.client.albums.find_one({"_owner_id": ObjectId("0" * 24)})

    response = app.test_client().get(
        f"/albums/{album.get('_id')}/{'0' * 24}/low",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 404


def test_get_deleted_image_from_album():
    album = db.client.albums.find_one(
        {"_owner_id": ObjectId("663a200fcb14e84e2fff0db8")}
    )

    db.client.albums.update_one(
        {"_id": album.get("_id")},
        {"$set": {"pictures_ids": [ObjectId("0" * 24)]}},
    )

    response = app.test_client().get(
        f"/albums/{album.get('_id')}/{'0' * 24}",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 404


def test_get_low_res_deleted_image_from_album():
    album = db.client.albums.find_one(
        {"_owner_id": ObjectId("663a200fcb14e84e2fff0db8")}
    )

    response = app.test_client().get(
        f"/albums/{album.get('_id')}/{'0' * 24}/low",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 404


def test_get_image_album_with_no_right():
    album = db.client.albums.find_one({"_owner_id": ObjectId("0" * 24)})
    picture = db.client.pictures.find_one({"_owner_id": ObjectId("0" * 24)})

    db.client.albums.update_one(
        {"_id": album.get("_id")},
        {"$set": {"viewers_ids": []}},
    )

    response = app.test_client().get(
        f"/albums/{album.get('_id')}/{picture.get('_id')}",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 403


def test_get_low_res_image_album_with_no_right():
    album = db.client.albums.find_one({"_owner_id": ObjectId("0" * 24)})
    picture = db.client.pictures.find_one({"_owner_id": ObjectId("0" * 24)})

    response = app.test_client().get(
        f"/albums/{album.get('_id')}/{picture.get('_id')}/low",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 403
