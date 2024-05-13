import re

import pytest
from bson import ObjectId

from utils import app, auth, db, regex

token = None


@pytest.fixture(autouse=True, scope="module")
def get_token():
    global token

    token = auth.generate_token(ObjectId("663a200fcb14e84e2fff0db8"))

    yield

    token = None


def test_get_me():
    response = app.test_client().get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json.get("id") == "663a200fcb14e84e2fff0db8"
    assert response.json.get("username") == "test"
    assert response.json.get("email") == "test@a.co"
    assert response.json.get("password") is None


def test_update_password():
    response = app.test_client().patch(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "old_password": "tesT1234!",
            "new_password": "tesT1234!new",
        },
    )

    assert response.status_code == 200
    assert response.json.get("id") == "663a200fcb14e84e2fff0db8"
    assert response.json.get("username") == "test"
    assert response.json.get("email") == "test@a.co"
    assert response.json.get("password") is None

    response = app.test_client().post(
        "/auth/login",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "login": "test@a.co",
            "password": "tesT1234!new",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    assert re.match(
        regex.isJWT,
        response.json.get("access_token"),
    )


def test_update_password_wrong_password():
    response = app.test_client().patch(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "old_password": "tesT1234!wrong",
            "new_password": "tesT1234!new",
        },
    )

    assert response.status_code == 401


def test_update_user():
    response = app.test_client().put(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "test_updated",
            "email": "test_updated@example.com",
        },
    )

    assert response.status_code == 200
    assert response.json.get("id") == "663a200fcb14e84e2fff0db8"
    assert response.json.get("username") == "test_updated"
    assert response.json.get("email") == "test_updated@example.com"
