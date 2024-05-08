import os
import sys

import pytest
from bson import ObjectId

print(os.getenv("IS_CI"))
if not os.getenv("IS_CI"):
    import routes
    from utils import app, db
else:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    print(sys.path)
    import routes
    from utils import app, db


@pytest.fixture(
    scope="session",
    autouse=True,
)
def set_test_env():
    os.environ["ENV"] = "TEST"
    os.environ["DB_NAME"] = "TestDatabase"
    os.environ["SECRET_KEY"] = "test_secret_key"

    print("Setting up test environment")

    db.init_db_client()

    routes.init_routes()

    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app

    db.db.drop_database(os.getenv("DB_NAME"))


@pytest.fixture(autouse=True, scope="module")
def create_collection():
    db.client.create_collection("users")
    db.client.users.insert_one(
        {
            "_id": ObjectId("663a200fcb14e84e2fff0db8"),
            "username": "test",
            "password": "$2b$12$srElp3FcISlRlcG1HY3tAOMQbOTuKEUVxHFQHTahH/oSc1QDYLkGi",
            "email": "test@a.co",
        }
    )

    yield

    db.client.drop_collection("users")
