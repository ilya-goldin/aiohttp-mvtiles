from .views import Handler


def frontend_routes(application):
    """
    Append frontend routes and middleware
    :param application:
    :type application: aiohttp.web.Application
    """
    application.router.add_get("/", Handler)
