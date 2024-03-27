import os

import pytest

from utils.db import client


@pytest.fixture(
    autouse=True,
)
def set_test_env():
    os.environ["ENV"] = "TEST"
    os.environ["DB_NAME"] = "TestDatabase"

    yield

    client.drop_database("TestDatabase")


def test_default():
    assert "test" == "test"


def test_insert():
    db = client[os.getenv("DB_NAME")]
    collection = db["test"]
    collection.insert_one({"name": "test"})
    assert collection.count_documents({}) == 1
