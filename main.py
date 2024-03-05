import os
from utils import loggingConfig
import dotenv

if __name__ == "__main__":
    loggingConfig.setupLogging()
    # import routes
    from routes import app

    dotenv.load_dotenv()
    app.run(debug=os.getenv("ENV") != "production")
