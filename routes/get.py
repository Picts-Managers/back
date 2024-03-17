import os
from middlewares import schema
from utils import app, route
from flask import request

from schemas import test

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

@route("/test/<testParam>")
@schema(test)
def testEndpoint(testParam: str):
    print(request.query.test)
    return {"test": testParam}