from aiohttp.web import View, Response
from db.sql import get_tile_bounds


class MVTView(View):
    async def get(self):
        """
        GET request MVT file

        :return: Response with mvt file (bytes)
        :rtype: Response
        """
        params = self.request.rel_url.query
        z, x, y = None, None, None
        if 'tile' in params:
            zxy = params.get('tile', '').split('/')
            if len(zxy) == 3:
                z = int(zxy[0])
                x = int(zxy[1])
                y = int(zxy[2])
        elif self.request.match_info:
            z = int(self.request.match_info.get('z', None))
            x = int(self.request.match_info.get('x', None))
            y = int(self.request.match_info.get('y', None))

        if z and x and y:
            db = self.request.app['db']
            query = get_tile_bounds(z, x, y) + self.request.app['tile_query']
            mvt = await db.fetch(query)
            status = 200 if mvt else 204
        else:
            mvt = b""
            status = 400
        response = Response(
            body=mvt,
            status=status,
            content_type="application/vnd.mapbox-vector-tile",
        )
        return response
