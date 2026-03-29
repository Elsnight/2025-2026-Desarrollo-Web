import os
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    DATABASE_PATH = DATA_DIR / "faustos_coffee.sqlite3"
    SECRET_KEY = os.environ.get("SECRET_KEY", "faustos-coffee-dev")
