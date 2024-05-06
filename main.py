import os

import dotenv

from utils import loggingConfig, swagger

if __name__ == "__main__":
    dotenv.load_dotenv()
    loggingConfig.setupLogging()
    import routes
    from utils import app

    routes.init_routes()
    swagger.init_swagger()

    app.run(debug=os.getenv("ENV") != "production", port=3000)
