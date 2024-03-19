import os
from utils import app, route


@route("/")
def index():
    if os.getenv("ENV") == "production":
        return "Welcome to our Picts manager API"
    routes = []
    for route in app.url_map.iter_rules():
        if route.rule.startswith("/static"):
            continue

        routes.append(
            {
                "route": route.rule,
                "method": [
                    method
                    for method in route.methods
                    if method not in ["HEAD", "OPTIONS"]
                ][0],
            }
        )
    routes = sorted(
        routes,
        key=lambda x: (x["route"], x["method"]),
    )
    return routes
