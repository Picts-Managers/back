import logging

from utils import loggingConfig

loggingConfig.setupLogging()

import routes  # noqa: E402, F401
from utils import app  # noqa: E402

if __name__ == "__main__":
    app.run()
else:
    __logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = __logger.handlers
