import os
import bcrypt
from bson import ObjectId
from flask import abort
import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def encrypt_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

def generate_token(id: ObjectId) -> str:
    return jwt.encode({"id": str(id)}, SECRET_KEY, algorithm=ALGORITHM)

def check_token(token: str) -> ObjectId:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return ObjectId(payload["id"])
    except jwt.ExpiredSignatureError:
        return abort(401, description="expired_token")
    except jwt.InvalidTokenError:
        return abort(401, description="invalid_token")
