import os

import dotenv

from utils import loggingConfig, swagger
from utils.db import init_db_client

if __name__ == "__main__":
    dotenv.load_dotenv()
    loggingConfig.setupLogging()
    import routes
    from utils import app

    init_db_client()
    routes.init_routes()
    swagger.init_swagger()

    app.run(debug=os.getenv("ENV") != "production", port=3000)
