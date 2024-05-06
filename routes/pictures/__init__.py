from flask import Blueprint

from .get import blueprint as get
from .post import blueprint as post
from .patch import blueprint as patch
from .delete import blueprint as delete


blueprint = Blueprint("pictures", __name__, url_prefix="/pictures")

blueprint.register_blueprint(get)
blueprint.register_blueprint(post)
blueprint.register_blueprint(patch)
blueprint.register_blueprint(delete)
