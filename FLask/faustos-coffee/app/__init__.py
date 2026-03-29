from pathlib import Path

from flask import Flask

from config import Config
from . import models  # noqa: F401
from .extensions import db, login_manager
from .models import Usuario
from .routes import register_routes
from .services.catalog_service import CatalogService
from .services.file_service import FileService
from .services.inventario import Inventario
from .services.pdf_service import ProductReportService


@login_manager.user_loader
def load_user(user_id: str):
    if not user_id.isdigit():
        return None
    return db.session.get(Usuario, int(user_id))


def create_app(config_class=Config):
    base_dir = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        template_folder=str(base_dir / "templates"),
        static_folder=str(base_dir / "static"),
        static_url_path="/static",
    )
    app.config.from_object(config_class)

    app.config["DATA_DIR"].mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)

    inventario = Inventario()
    file_service = FileService(app.config["DATA_DIR"])
    catalog_service = CatalogService(inventario, file_service)
    product_report_service = ProductReportService()

    app.extensions["inventario"] = inventario
    app.extensions["file_service"] = file_service
    app.extensions["catalog_service"] = catalog_service
    app.extensions["product_report_service"] = product_report_service

    with app.app_context():
        catalog_service.initialize_catalog()

    register_routes(app)
    return app
