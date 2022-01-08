from os import path, getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")
POSTGIS_3 = True

TEMPLATES_DIR = path.join("apps", "frontend", "templates")

STATIC_DIR = path.join("apps", "frontend", "static")
STATIC_URL = "/static"

CORS_ALLOW_ORIGINS = ["https://frontend.com"]
