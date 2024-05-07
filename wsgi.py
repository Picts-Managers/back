import logging

from routes import init_routes
from utils import app, loggingConfig

loggingConfig.setupLogging()
init_routes()


if __name__ == "__main__":
    app.run()
else:
    __logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = __logger.handlers
