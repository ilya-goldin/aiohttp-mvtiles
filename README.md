
# aiohttp-mvtiles

A simple Mapbox Vector Tiles server. Based on aiohttp


## Features

- Generating a single or multi-layered [MVT](https://mapbox.github.io/vector-tile-spec/) file  with [PostGIS](https://postgis.net/)
- Generating tiles with the necessary parameters and layer names from the database
## Installation
Clone the project
```bash
  git clone https://github.com/ilya-goldin/aiohttp-mvtiles.git
```
Go to the project directory
```bash
  cd aiohttp-mvtiles
```
Install dependencies
```bash
  pip install -r requirements.txt 
```
Start the server

```bash
  python main.py
  ```
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DATABASE_URL`
## Usage
### Create layer classes in models.py
```python
ExampleLayer = LayerModel(
    table_name="boundaries",
    geom_column="geom",
    layer_column="layer",
    include_columns=["name", "population"]
)
```
### Set the configuration in the settings.py file:
```python
# PostgreSQL with PostGIS version 3 support?
POSTGIS_3 = True

# List of layer classes from the models.py file
LAYERS = [ExampleLayer]

# SRID of a field with geometry in the database
LAYERS_SRID = 4326

# The tile extent in tile coordinate space
EXTEND = 4096

# The buffer distance in tile coordinate space to optionally clip geometries
BUFFER = 256

# A boolean to control if geometries should be clipped or encoded as is
CLIP = False
```


## API Reference

#### Get tile by [XYZ](https://en.wikipedia.org/wiki/Tiled_web_map#Tile_numbering_schemes) params

```http
  GET /api/v1/tile/{z}/{x}/{y} or /api/v1/t.mvt?tile={z}/{x}/{y}
```

| Parameter | Type  | Description                |
|:----------|:------|:---------------------------|
| `z`       | `int` | **Required**. Zoom level   |
| `x`       | `int` | **Required**. X tile coord |
| `y`       | `int` | **Required**. Y tile coord |
