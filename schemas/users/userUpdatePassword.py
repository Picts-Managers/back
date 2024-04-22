import re

from pydantic import BaseModel, field_validator

from utils.regex import isPassword


class Request(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    def password_length(cls, v):
        if re.match(isPassword, v):
            return v
        raise ValueError(
            "Password must be at least 8 characters long and contain at least one letter and one number."
        )


class Response(BaseModel):
    username: str
    email: str
    id: str
