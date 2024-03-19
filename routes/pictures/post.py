from datetime import datetime

from bson import ObjectId
from flask import request
from PIL import Image

from middlewares import schema
from middlewares.auth import isLogged
from models import Picture
from repositories import picture_repository
from utils import route
from utils.image import get_metadata
from schemas.pictures import createPicture


@route("/")
@isLogged
@schema(createPicture)
def index():
    uploaded_file = request.files["file"]
    image = Image.open(uploaded_file)
    filename = ".".join(uploaded_file.filename.split(".")[:-1])
    metadata = get_metadata(image)
    picture = Picture(
        owner_id=request.req_user.id,
        location=metadata.get("location", None),
        date=metadata.get("date", datetime.now().isoformat()),
        filename=filename,
        mimetype=uploaded_file.mimetype,
    )
    picture = picture_repository.insertPicture(picture)

    if uploaded_file.mimetype == "image/png":
        white_image = Image.new("RGBA", image.size, "WHITE")
        white_image.paste(image, mask=image)
        image = white_image.convert("RGB")

    image.save(f"uploads/{picture.id}", "JPEG")
    image.thumbnail((200, 200))
    image.save(f"uploads/{picture.id}.low", "JPEG")

    return picture
