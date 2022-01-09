from os import path, getenv
from dotenv import load_dotenv
from db.models import ExampleLayer

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")
POSTGIS_3 = True

LAYERS = [ExampleLayer]
LAYERS_SRID = 4326
EXTEND = 4096
BUFFER = 256
CLIP = False


TEMPLATES_DIR = path.join("apps", "frontend", "templates")

STATIC_DIR = path.join("apps", "frontend", "static")
STATIC_URL = "/static"
