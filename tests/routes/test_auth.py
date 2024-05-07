import re

import pytest
from bson import ObjectId

from utils import app, auth, regex

token = None


@pytest.fixture(autouse=True, scope="module")
def get_token():
    print("token")
    global token

    token = auth.generate_token(ObjectId("663a200fcb14e84e2fff0db8"))
    yield
    token = None


def test_register_success():
    response = app.test_client().post(
        "/auth/register",
        json={
            "email": "test@a.com",
            "username": "testa",
            "password": "tesT1234!",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    assert re.match(
        regex.isJWT,
        response.json.get("access_token"),
    )


def test_register_not_valid_password():
    response = app.test_client().post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "test",
            "password": "test",
        },
    )

    assert response.status_code == 400


def test_register_not_valid_email():
    response = app.test_client().post(
        "/auth/register",
        json={
            "email": "test",
            "username": "test",
            "password": "tesT1234!",
        },
    )

    assert response.status_code == 400


def test_register_not_valid_username():
    response = app.test_client().post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "te",
            "password": "tesT1234!",
        },
    )

    assert response.status_code == 400


def test_register_user_already_exists():
    response = app.test_client().post(
        "/auth/register",
        json={
            "email": "test@a.co",
            "username": "test",
            "password": "tesT1234!",
        },
    )
    assert response.status_code == 400


def test_login_with_email_success():
    response = app.test_client().post(
        "/auth/login",
        json={
            "login": "test@a.co",
            "password": "tesT1234!",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    assert re.match(
        regex.isJWT,
        response.json.get("access_token"),
    )


def test_with_username_success():
    response = app.test_client().post(
        "/auth/login",
        json={
            "login": "test",
            "password": "tesT1234!",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    assert re.match(
        regex.isJWT,
        response.json.get("access_token"),
    )


def test_login_with_token_success():
    response = app.test_client().post(
        "/auth/login-with-token",
        headers={
            "Authorization": "Bearer " + token,
        },
    )

    assert response.status_code == 200
    assert response.json.get("id") == "663a200fcb14e84e2fff0db8"
    assert response.json.get("username") == "test"
    assert response.json.get("email") == "test@a.co"
    assert response.json.get("password") is None
