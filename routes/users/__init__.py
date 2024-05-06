from flask import Blueprint

from .get import blueprint as get
from .put import blueprint as put
from .patch import blueprint as patch
from .delete import blueprint as delete


blueprint = Blueprint("users", __name__, url_prefix="/users")

blueprint.register_blueprint(get)
blueprint.register_blueprint(put)
blueprint.register_blueprint(patch)
blueprint.register_blueprint(delete)
