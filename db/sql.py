from settings import POSTGIS_3, LAYERS


def get_sql_query(srid=3857, extend=4096, buffer=256, clip=True):
    """
    Build basic SQL query string without tile bbox

    :param int srid: SRID of geometry
    :param int extend: The tile extent in tile coordinate space as defined by the specification. Default is 4096.
    :param int buffer: The buffer distance in tile coordinate space to optionally clip geometries. Default is 256.
    :param bool clip: A boolean to control if geometries should be clipped or encoded as is. Default is True
    :return: SQL query string
    :rtype: str
    """
    mvt_sql = ""
    union_sql = ""
    for idx, model in enumerate(LAYERS):
        mvt_sql += f""",
            {model.table_name}_mvt AS (
            SELECT id, {model.sql_layer}, {model.sql_columns}
                ST_AsMVTGeom(
                    ST_Transform(t.{model.geom_column}, 3857),
                    bounds.geom, {extend}, {buffer}, {clip}
                    ) AS geom
            FROM   {model.table_name} t, bounds
            WHERE  t.{model.geom_column} && ST_Transform(bounds.geom, {srid})
            )
            """
        union_sql += f"""
            {'UNION' if idx > 0 else ''}
            SELECT ST_AsMVT({model.table_name}_mvt.*, layer, {extend}, 'geom') AS mvt
            FROM {model.table_name}_mvt
            GROUP BY layer
            """
    query = f"""
        {mvt_sql}
        SELECT string_agg(mvt, '') AS mvt
        FROM (
            {union_sql}
        ) sub;
        """
    return query


def get_tile_bounds(z, x, y, srid=3857):
    """
    Get ST_MakeEnvelope from ZXY params, transform to given SRID

    :param int z: Zoom level
    :param int x: X tile coord
    :param int y: Y tile coord
    :param srid: SRID of bounds
    :type srid: int
    :return: String with Tile Envelope
    :rtype: str
    """
    if POSTGIS_3:
        bounds = f"ST_TileEnvelope({z}, {x}, {y})"
    else:
        max_coord = 20037508.34
        res = (max_coord * 2) / (2 ** z)
        bounds = f"ST_MakeEnvelope(" \
                 f"{- max_coord + (x * res)}, " \
                 f"{max_coord - (y * res)}, " \
                 f"{- max_coord + (x * res) + res}, " \
                 f"{max_coord - (y * res) - res}, 3857)"
    if srid != 3857:
        bounds = f"ST_Transform({bounds}, {srid})"
    result = f"WITH bounds(geom) AS (SELECT {bounds} as geom)"
    return result
