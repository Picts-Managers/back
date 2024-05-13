from flask import Blueprint, request

from middlewares import schema
from middlewares.auth import isLogged
from schemas.pictures import createPicture
from utils.image import handle_picture_upload

blueprint = Blueprint(__name__.replace(".", "/"), __name__)


@blueprint.post("/upload")
@isLogged
@schema(createPicture)
def index():
    uploaded_file = request.files["file"]
    picture = handle_picture_upload(uploaded_file)
    return picture
