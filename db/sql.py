from settings import POSTGIS_3

template = [
    {
        'name': 'world_bounds',
        'geom_column': 'geom',
        'layer_column': None,
        'include_columns': ['name', 'population'],
    }
]


class QueryMVT:
    def __init__(self, z, x, y, params, srid=3857, extend=4096, buffer=256, clip=True):
        """
        Mapbox Vector Tile query class

        :param z: Zoom level
        :type z: int
        :param x: X tile coord
        :type x: int
        :param y: Y tile coord
        :type y: int
        :param params: List of dictionaries defining the basic data for the tables to be exported to MVT file.
        :type params: list[dict[str, str]]
        :param srid: SRID of geometry
        :type srid: int
        :param extend: The tile extent in tile coordinate space as defined by the specification. Default is 4096.
        :type extend: int
        :param buffer: The buffer distance in tile coordinate space to optionally clip geometries. Default is 256.
        :type buffer: int
        :param clip: A boolean to control if geometries should be clipped or encoded as is. Default is True
        :type clip: bool
        """
        self.z = z
        self.x = x
        self.y = y
        self.tile_bounds = self.get_tile_bounds()
        self.params = params
        self.srid = srid
        self.extend = extend
        self.buffer = buffer
        self.clip = clip

    def get_sql_query(self):
        mvt_sql = ""
        union_sql = ""
        for idx, table in enumerate(self.params):
            mvt_sql += f""",
                {table['name']}_mvt AS (
                SELECT id, {self.get_layer_column(table)}, {self.get_include_columns(table)}
                    ST_AsMVTGeom(
                        ST_Transform(t.{table['geom_column']}, 3857),
                        bounds.geom, {self.extend}, {self.buffer}, {self.clip}
                        ) AS geom
                FROM   {table['name']} t, bounds
                WHERE  t.{table['geom_column']} && ST_Transform(bounds.geom, {self.srid})
                )
                """
            union_sql += f"""
                {'UNION' if idx > 0 else ''}
                SELECT ST_AsMVT({table['name']}_mvt.*, layer, {self.extend}, 'geom') AS mvt
                FROM {table['name']}_mvt
                GROUP BY layer
                """
        query = f"""
            {self.tile_bounds}
            {mvt_sql}
            SELECT string_agg(mvt, '') AS mvt
            FROM (
                {union_sql}
            ) sub;
            """
        return query

    def get_tile_bounds(self, srid=3857):
        """
        Get ST_MakeEnvelope from ZXY params, transform to given SRID

        :param srid: SRID of bounds
        :type srid: int
        :return: String with Tile Envelope
        """
        if POSTGIS_3:
            bounds = f"WITH bounds(geom) AS (SELECT ST_TileEnvelope({self.z}, {self.x}, {self.y}) as geom)"
        else:
            max_coord = 20037508.34
            res = (max_coord * 2) / (2 ** self.z)
            bounds = f"WITH bounds(geom) AS (SELECT ST_MakeEnvelope(" \
                     f"{- max_coord + (self.x * res)}, " \
                     f"{max_coord - (self.y * res)}, " \
                     f"{- max_coord + (self.x * res) + res}, " \
                     f"{max_coord - (self.y * res) - res}, 3857) as geom)"
        if srid != 3857:
            bounds = f"ST_Transform({bounds}, {self.srid})"
        return bounds

    def get_layer_column(self, table):
        if table["layer_column"]:
            layer = f"{table['layer_column']} AS layer"
        else:
            layer = f"{table['name']}_layer AS layer"
        return layer

    def get_include_columns(self, table):
        if table["include_columns"]:
            columns = ", ".join(table["include_columns"]) + ","
        else:
            columns = ""
        return columns
