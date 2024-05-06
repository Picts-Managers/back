import json
import os
import re
from importlib import import_module

from flasgger import Swagger

from utils import app
from utils.types import QueryType, RequestType, ResponseType, Schema

REFS_TO_IMPORT = set()


def _get_route_info(route: str):
    method = re.search(r"\.(\w+)\(", route).group(1) or "get"
    if method == "route":
        method = (
            re.search(r"methods=\[\"(.*?)\"\]", route).group(1).lower()
            if re.search(r"methods=\[\"(.*?)\"\]", route)
            else "get"
        )

    url = re.search(r"\"(.*?)\"", route).group(1).replace("<", "{").replace(">", "}")
    return (method, url)


def _parse_query_params_from_schema(querySchema: QueryType):
    params = []

    for key, info in querySchema.model_fields.items():
        params.append(
            {
                "name": key,
                "in": "query",
                "type": "string",
                "required": info.is_required(),
            }
        )
    return params


def _parse_body_params_from_schema(bodySchema: RequestType):
    params = {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": bodySchema.model_json_schema().get("properties", {}),
                },
            },
        },
    }

    return params


def _parse_response_from_schema(responseSchema: ResponseType):
    params = responseSchema.model_json_schema().get("properties", {})

    dumped = json.dumps(params)
    res = re.findall(r'{"\$ref": "#/\$defs/(.*?)"}', dumped)
    if res:
        REFS_TO_IMPORT.update(res)

    return params


def _get_route_params(url: str, schema: Schema):
    params = [
        (
            {
                "name": param,
                "in": "path",
                "type": "string",
                "required": True,
            }
        )
        for param in re.findall(r"{(.*?)}", url)
    ]

    if hasattr(schema, "Query"):
        params += _parse_query_params_from_schema(schema.Query)

    return params


def _get_route_responses(responseSchema: ResponseType):
    return {
        "200": {
            "description": "Success",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": (
                            _parse_response_from_schema(responseSchema.Response)
                            if responseSchema and hasattr(responseSchema, "Response")
                            else {}
                        ),
                    },
                },
            },
        },
        "304": {
            "description": "Not Modified",
        },
        "400": {
            "description": "Bad Request",
        },
        "401": {
            "description": "Unauthorized",
        },
        "403": {
            "description": "Forbidden",
        },
        "404": {
            "description": "Not Found",
        },
        "405": {
            "description": "Method Not Allowed",
        },
        "500": {
            "description": "Internal Server Error",
        },
    }


def _get_schema(middleware):
    schema = re.search(r"\((.*?)\)", middleware).group(1)

    for root, _, file in os.walk("./schemas"):
        if f"{schema}.py" in file:
            schema = import_module(f"{root[2:].replace('/', '.')}.{schema}")

    return schema


def _get_middlewares(lines: list[str], start_index: int):
    middlewares = []
    index = start_index + 1
    while not lines[index].startswith("def"):
        middlewares.append(lines[index][1:].replace("\n", ""))
        index += 1
    return middlewares


def _generate_specs():
    routes_folder = "./routes"
    specs = {}

    for root, _, files in os.walk(routes_folder):
        tag = root[len(routes_folder) + 1 :] or "Root"

        for file in files:
            if not file.endswith(".py") or file == "__init__.py":
                continue
            lines = []
            with open(f"{root}/{file}", "r") as f:
                lines = f.readlines()
            routes = [
                (index, line[1:])
                for index, line in enumerate(lines)
                if line.startswith("@blueprint")
            ]

            for start_index, line in routes:
                middlewares = _get_middlewares(lines, start_index)
                method, url = _get_route_info(line)
                specs.setdefault(
                    f"{('/' + tag if tag != 'Root' else '')}{url}",
                    {},
                )

                schema = None

                for middleware in middlewares:
                    if middleware.startswith("schema"):
                        schema = _get_schema(middleware)
                        break

                specs[f"{('/' + tag if tag != 'Root' else '')}{url}"][method] = {
                    "tags": [tag.capitalize()],
                    "parameters": _get_route_params(url, schema) if schema else [],
                    "requestBody": (
                        _parse_body_params_from_schema(schema.Request)
                        if hasattr(schema, "Request")
                        else {}
                    ),
                    "responses": _get_route_responses(schema),
                    "security": [{"Bearer": []}] if "isLogged" in middlewares else [],
                }

    return specs


def _generate_template():
    template = {}
    with open("documentation/template.json", "r") as file:
        template = json.load(file)

    template["paths"] = _generate_specs()

    if len(REFS_TO_IMPORT):
        type_file = import_module("utils.types")

        for ref in REFS_TO_IMPORT:
            template.setdefault("$defs", {})
            template["$defs"][ref] = type_file.__dict__[ref].model_json_schema()
    print(template["components"])
    return template


def init_swagger():
    app.config["SWAGGER"] = {
        "openapi": "3.0.3",
        "specs_route": "/",
    }
    Swagger(
        app,
        template=_generate_template(),
    )
