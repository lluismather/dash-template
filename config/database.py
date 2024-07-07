
import os
from dotenv import load_dotenv

load_dotenv()

def update_db_url(db_url):
    return db_url if db_url.startswith("postgresql") else "postgresql" + db_url[8:]

DATABASE_URL = update_db_url(os.getenv("DATABASE_URL", "sqlite:///db.sqlite"))
