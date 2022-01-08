from .views import MVTView


def api_routes(application, cors):
    """
    Append api routes and middleware
    :param application:
    :type application: aiohttp.web.Application
    """
    api1 = cors.add(application.router.add_resource("/api/v1/t.mvt"))
    api2 = cors.add(application.router.add_resource(r"/api/v1/tile/{z:\d+}/{x:\d+}/{y:\d+}"))
    cors.add(api1.add_route("GET", MVTView))
    cors.add(api2.add_route("GET", MVTView))

