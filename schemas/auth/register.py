import re

from pydantic import BaseModel, Field, field_validator

from utils.regex import isEmail, isJWT, isPassword, isUsername


class Request(BaseModel):
    username: str = Field(pattern=isUsername)
    password: str
    email: str = Field(pattern=isEmail)

    @field_validator("password")
    def password_length(cls, v):
        if re.match(isPassword, v):
            return v
        raise ValueError(
            "Password must be at least 8 characters long and contain at least one letter and one number."
        )


class Response(BaseModel):
    access_token: str = Field(pattern=isJWT)
