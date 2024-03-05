import os
from utils import loggingConfig
import dotenv

if __name__ == "__main__":
    dotenv.load_dotenv()

    loggingConfig.setupLogging()

    # import routes
    from routes import app

    app.run(debug=os.getenv("ENV") != "production")
