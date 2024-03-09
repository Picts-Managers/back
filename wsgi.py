from utils import loggingConfig
import logging

loggingConfig.setupLogging()


import routes
from utils import app

if __name__ == "__main__":
    app.run()
else:
    __logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = __logger.handlers
