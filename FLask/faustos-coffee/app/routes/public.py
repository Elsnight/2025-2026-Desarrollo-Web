from flask import current_app, flash, redirect, render_template, url_for


def _catalog_service():
    return current_app.extensions["catalog_service"]


def register_public_routes(app):
    @app.get("/")
    def home():
        productos = _catalog_service().list_products()
        producto_destacado = productos[0] if productos else None
        return render_template(
            "index.html",
            productos=productos,
            producto_destacado=producto_destacado,
        )

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.get("/productos")
    def productos():
        return render_template(
            "productos.html",
            productos=_catalog_service().list_products(),
            producto_destacado=None,
        )

    @app.get("/productos/archivos")
    def archivos_productos():
        _catalog_service().sync_flat_files()
        return render_template(
            "archivos_productos.html",
            productos=_catalog_service().list_products(),
            archivos=_catalog_service().get_files_report(),
        )

    @app.get("/producto/<slug>")
    def producto(slug):
        producto_encontrado = _catalog_service().get_product_by_slug(slug)

        if producto_encontrado is None:
            flash("El producto solicitado no existe en el inventario actual.", "warning")
            return redirect(url_for("productos"))

        return render_template(
            "productos.html",
            productos=_catalog_service().list_products(),
            producto_destacado=producto_encontrado,
        )
