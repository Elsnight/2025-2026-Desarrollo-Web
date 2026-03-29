import os
from pathlib import Path
from urllib.parse import quote_plus


def build_database_uri(base_dir: Path) -> tuple[str, str]:
    database_engine = os.environ.get("DATABASE_ENGINE", "sqlite").strip().lower()

    if database_engine == "mysql":
        mysql_user = os.environ.get("MYSQL_USER", "root").strip()
        mysql_password = os.environ.get("MYSQL_PASSWORD", "")
        mysql_host = os.environ.get("MYSQL_HOST", "localhost").strip()
        mysql_port = os.environ.get("MYSQL_PORT", "3306").strip()
        mysql_database = os.environ.get("MYSQL_DATABASE", "faustos_coffee").strip()

        credenciales = quote_plus(mysql_user)
        if mysql_password:
            credenciales = f"{credenciales}:{quote_plus(mysql_password)}"

        return (
            f"mysql+pymysql://{credenciales}@{mysql_host}:{mysql_port}/{mysql_database}?charset=utf8mb4",
            "MySQL",
        )

    sqlite_database_path = (base_dir / "data" / "faustos_coffee.sqlite3").resolve()
    return f"sqlite:///{sqlite_database_path.as_posix()}", "SQLite"


class Config:
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    SQLALCHEMY_DATABASE_URI, DATABASE_BACKEND = build_database_uri(BASE_DIR)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "faustos-coffee-dev")
