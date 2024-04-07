import os

import dotenv

from utils import loggingConfig

if __name__ == "__main__":
    dotenv.load_dotenv()
    loggingConfig.setupLogging()
    import routes  # noqa: F401
    from utils import app

    app.run(debug=os.getenv("ENV") != "production", port=3000)
