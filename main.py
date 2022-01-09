from aiohttp import web
import jinja2
import aiohttp_jinja2


def setup_routes(app):
    """Setup module routes for application

    :param web.Application app: aiohttp Application class
    """
    from aiohttp_cors import setup, ResourceOptions
    from apps.api.routes import api_routes
    from apps.frontend.routes import frontend_routes
    cors = setup(app, defaults={
        "http://0.0.0.0:8080": ResourceOptions()
    })
    api_routes(app, cors)
    frontend_routes(app)


def setup_external_libraries(app):
    """Setup static libraries roots for jinja2.

    :param web.Application app: aiohttp Application class
    """
    from settings import STATIC_DIR, STATIC_URL, TEMPLATES_DIR
    aiohttp_jinja2.setup(
        app,
        enable_async=True,
        loader=jinja2.FileSystemLoader(TEMPLATES_DIR))
    app.add_routes([web.static(
        STATIC_URL,
        STATIC_DIR
    )])
    app['static_root_url'] = STATIC_URL


async def on_startup(app):
    """Init DB connection pool on start up

    :param web.Application app: aiohttp Application class
    """
    from db.db import Database
    from db.sql import get_sql_query
    from settings import DATABASE_URL, LAYERS_SRID, EXTEND, BUFFER, CLIP
    app['db'] = Database(DATABASE_URL)
    await app['db'].connect()
    print("Server Startup")
    app['tile_query'] = get_sql_query(srid=LAYERS_SRID, extend=EXTEND, buffer=BUFFER, clip=CLIP)


async def on_cleanup(app):
    """Close DB connection on cleanup

    :param web.Application app: Application
    """
    await app['db'].close()
    print("Server Shutdown")


async def init_app():
    """
    Initialize application

    :return: Application
    :rtype: web.Application
    """
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    setup_external_libraries(app)
    setup_routes(app)
    return app


if __name__ == "__main__":
    application = init_app()
    web.run_app(application)
