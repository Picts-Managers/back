from utils import loggingConfig
from routes import app

if __name__ == "__main__":
    loggingConfig.setupLogging()

    app.run()
