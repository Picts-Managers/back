import logging
from utils import loggingConfig


if __name__ == "__main__":

    loggingConfig.setupLogging()
    import routes

    routes.app.run(debug=True)
