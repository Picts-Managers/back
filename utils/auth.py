import os

import bcrypt
import jwt
from bson import ObjectId
from flask import abort

ALGORITHM = "HS256"


def encrypt_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode())


def generate_token(id: ObjectId) -> str:
    return jwt.encode({"id": str(id)}, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)


def check_token(token: str) -> ObjectId:
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=ALGORITHM)
        return ObjectId(payload["id"])
    except jwt.ExpiredSignatureError:
        return abort(401, description="expired_token")
    except jwt.InvalidTokenError:
        return abort(401, description="invalid_token")
