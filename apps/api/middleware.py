from aiohttp.web import Request, Response, json_response
from aiohttp_middlewares import error_context


async def api_error(request: Request) -> Response:
    with error_context(request) as context:
        return json_response(
            context.data, status=context.status
        )
