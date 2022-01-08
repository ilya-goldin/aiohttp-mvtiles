from re import compile
from .views import Handler
from aiohttp_middlewares import cors_middleware
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS
from settings import CORS_ALLOW_ORIGINS


def frontend_routes(app):
    """
    Append frontend routes and middleware
    :param app:
    :type app: aiohttp.web.Application
    """
    app.router.add_get("/", Handler)
    app.middlewares.append(
        cors_middleware(
            origins=[compile(r"^https?\:\/\/localhost")] + CORS_ALLOW_ORIGINS,
            allow_methods=["GET"],
            allow_headers=DEFAULT_ALLOW_HEADERS,
        )
    )
