from pydantic import BaseModel, Field


class Query(BaseModel):
    test: str = Field(title="Test", description="Test query parameter")

# class Request(BaseModel):
#     pass

# class Response(BaseModel):
#     pass