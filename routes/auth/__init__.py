from flask import Blueprint

from .post import blueprint as post


blueprint = Blueprint("auth", __name__, url_prefix="/auth")

blueprint.register_blueprint(post)
