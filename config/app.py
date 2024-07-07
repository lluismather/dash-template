
import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "local")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "secret")
APP_DEBUG = os.getenv("APP_DEBUG", False)
APP_HOST = os.getenv("APP_HOST", "localhost")
APP_PORT = os.getenv("APP_PORT", "8000")
APP_URL = os.getenv("APP_URL", "http://localhost:8000")
