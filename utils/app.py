import json
from flask import Flask, Response
from pydantic import BaseModel

from werkzeug.exceptions import HTTPException
from utils.MongoJSONProvider import MongoJSONProvider

from flask_cors import CORS
from pillow_heif import register_heif_opener


class App(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_response(self, rv) -> Response:
        if issubclass(type(rv), BaseModel):
            rv = rv.model_dump()
        return super().make_response(rv)


app = App(__name__)
app.json = MongoJSONProvider(app)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

register_heif_opener()


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps(
        {
            "status": e.code,
            "error": e.description,
        }
    )
    response.content_type = "application/json"
    return response
