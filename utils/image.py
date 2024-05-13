from datetime import datetime

from flask import request
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS
from PIL.Image import Exif
from PIL.Image import Image as ImageType
from werkzeug.datastructures import FileStorage

from models import Picture
from repositories import picture_repository


def _get_geotagging(exif: Exif):
    exif = exif.get_ifd(0x8825)
    geo_tagging_info = {}
    if not exif:
        return {}

    for k, v in exif.items():
        try:
            geo_tagging_info[GPSTAGS[k]] = str(v)
        except IndexError:
            pass
    return geo_tagging_info


def _parse_gps_coordinates(gps_data):
    latitude = gps_data.get("GPSLatitude")
    longitude = gps_data.get("GPSLongitude")
    lat_ref = gps_data.get("GPSLatitudeRef")
    long_ref = gps_data.get("GPSLongitudeRef")

    if latitude and longitude and lat_ref and long_ref:
        lat_deg, lat_min, lat_sec = eval(latitude)
        long_deg, long_min, long_sec = eval(longitude)

        # Calculate decimal degrees
        latitude_decimal = lat_deg + lat_min / 60.0 + lat_sec / 3600.0
        longitude_decimal = long_deg + long_min / 60.0 + long_sec / 3600.0

        # Set negative for South latitude and West longitude
        if lat_ref == "S":
            latitude_decimal *= -1
        if long_ref == "W":
            longitude_decimal *= -1

        return str(latitude_decimal), str(longitude_decimal)
    else:
        return None, None


def get_metadata(image: ImageType) -> dict:
    exif = image.getexif()
    if exif is None:
        return {}
    parsed = {TAGS.get(tag, tag): value for tag, value in exif.items()}
    date = parsed.get("DateTime")
    if date:
        parsed["date"] = datetime.strptime(date, "%Y:%m:%d %H:%M:%S").isoformat()
    gps_info = _get_geotagging(exif)
    if not gps_info:
        return parsed

    lat, long = _parse_gps_coordinates(gps_info)
    if lat and long:
        parsed["location"] = {"latitude": lat, "longitude": long}
    return parsed


def compress_image(image: ImageType) -> ImageType:
    if image.mode == "RGBA" or image.mode == "P":
        if image.mode == "P":
            image = image.convert("RGBA")

        white_image = Image.new("RGBA", image.size, "WHITE")
        white_image.paste(image, mask=image)
        image = white_image.convert("RGB")
    return image


def handle_picture_upload(uploaded_file: FileStorage):
    with Image.open(uploaded_file) as image:
        filename = ".".join(uploaded_file.filename.split(".")[:-1])
        metadata = get_metadata(image)
        picture = Picture(
            owner_id=request.req_user.id,
            location=metadata.get("location", None),
            date=metadata.get("date", datetime.now().isoformat()),
            filename=filename,
            mimetype="image/jpeg",
        )
        picture = picture_repository.insertPicture(picture)

        image = compress_image(image)

        image.save(f"uploads/{picture.id}", "JPEG", quality=50)
        image.thumbnail((200, 200))
        image.save(f"uploads/{picture.id}.low", "JPEG")

        return picture
