from .admin import register_admin_routes
from .public import register_public_routes


def register_routes(app):
    register_public_routes(app)
    register_admin_routes(app)
