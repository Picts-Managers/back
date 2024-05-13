import logging

from routes import init_routes
from utils import app, loggingConfig
from utils.db import init_db_client

loggingConfig.setupLogging()
init_db_client()
init_routes()


if __name__ == "__main__":
    app.run()
else:
    __logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = __logger.handlers
