from datetime import datetime
from bson import ObjectId
from flask import request
from models import Picture

from repositories import picture_repository
from utils import route
from PIL import Image

from utils.image import get_metadata


@route("/")
def index():
    uploaded_file = request.files["file"]
    image = Image.open(uploaded_file)
    filename = ".".join(uploaded_file.filename.split(".")[:-1])
    metadata = get_metadata(image)
    picture = Picture(
        _id=ObjectId(),
        _owner_id=ObjectId("65e73cb103d93e117cadf9a9"),
        date=metadata.get("date", datetime.now().isoformat()),
        filename=filename,
        mimetype=uploaded_file.mimetype,
    )
    if metadata.get("location"):
        picture.location = metadata["location"]
    picture = picture_repository.insertPicture(picture)

    image.convert("RGB").save(f"uploads/{picture.id}", "JPEG")

    # pictures = picture_repository.insertPicture()
    return picture
