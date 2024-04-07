from pydantic import BaseModel


class Response(BaseModel):
    username: str
    email: str
    id: str
