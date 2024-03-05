import os
from utils import app


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
    # sort by GET, POST, PUT, PATCH, DELETE and by route length
    routes = sorted(
        routes,
        key=lambda x: (x["method"], x["route"]),
    )
    return routes
