from datetime import datetime

from PIL.ExifTags import GPSTAGS, TAGS
from PIL.Image import Exif
from PIL.Image import Image as ImageType
from werkzeug.datastructures import FileStorage


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
