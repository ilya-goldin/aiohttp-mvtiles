from aiohttp.web import View
import aiohttp_jinja2


class Handler(View):
    async def get(self):
        context = {
            'title': 'Simple aiohttp Mapbox Vector Tiles server',
            'colors': []
        }
        response = await aiohttp_jinja2.render_template_async(
            'index.html',
            self.request,
            context,
            status=200
        )
        response.headers['Content-Language'] = 'ru'
        return response
