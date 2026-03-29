from io import BytesIO

from flask import current_app, flash, redirect, render_template, request, send_file, url_for
from flask_login import login_required

from app.forms import build_product_from_form


def _catalog_service():
    return current_app.extensions["catalog_service"]


def _product_report_service():
    return current_app.extensions["product_report_service"]


def register_admin_routes(app):
    @app.get("/admin/productos")
    @login_required
    def admin_productos():
        producto_id = request.args.get("editar", type=int)
        producto_editar = None

        if producto_id is not None:
            producto_editar = _catalog_service().get_product_by_id(producto_id)
            if producto_editar is None:
                flash("El producto que intentas editar no existe.", "warning")
                return redirect(url_for("admin_productos"))

        return render_template(
            "admin_productos.html",
            productos=_catalog_service().list_products(),
            producto_editar=producto_editar,
        )

    @app.post("/admin/productos/crear")
    @login_required
    def crear_producto():
        producto, errores = build_product_from_form(request.form)

        if errores:
            for error in errores:
                flash(error, "danger")
            return redirect(url_for("admin_productos"))

        try:
            _catalog_service().create_product(producto)
        except ValueError as error:
            flash(str(error), "danger")
            return redirect(url_for("admin_productos"))

        flash("Producto creado correctamente en la base de datos.", "success")
        return redirect(url_for("admin_productos"))

    @app.post("/admin/productos/<int:producto_id>/editar")
    @login_required
    def editar_producto(producto_id):
        producto_existente = _catalog_service().get_product_by_id(producto_id)

        if producto_existente is None:
            flash("El producto a editar no fue encontrado.", "warning")
            return redirect(url_for("admin_productos"))

        producto, errores = build_product_from_form(request.form)

        if errores:
            for error in errores:
                flash(error, "danger")
            return redirect(url_for("admin_productos", editar=producto_id))

        try:
            _catalog_service().update_product(producto_id, producto)
        except ValueError as error:
            flash(str(error), "danger")
            return redirect(url_for("admin_productos", editar=producto_id))

        flash("Producto actualizado correctamente.", "success")
        return redirect(url_for("admin_productos"))

    @app.post("/admin/productos/<int:producto_id>/eliminar")
    @login_required
    def eliminar_producto(producto_id):
        producto_existente = _catalog_service().get_product_by_id(producto_id)

        if producto_existente is None:
            flash("El producto a eliminar no existe.", "warning")
            return redirect(url_for("admin_productos"))

        _catalog_service().delete_product(producto_id)
        flash("Producto eliminado del inventario.", "success")
        return redirect(url_for("admin_productos"))

    @app.post("/admin/productos/exportar-archivos")
    @login_required
    def exportar_archivos_productos():
        _catalog_service().sync_flat_files()
        flash("Archivos TXT, JSON y CSV actualizados correctamente.", "success")
        return redirect(url_for("archivos_productos"))

    @app.get("/admin/productos/reporte.pdf")
    @login_required
    def descargar_reporte_productos():
        productos = _catalog_service().list_products()

        if not productos:
            flash("No hay productos disponibles para generar el reporte PDF.", "warning")
            return redirect(url_for("admin_productos"))

        pdf_bytes = _product_report_service().build_products_pdf(
            productos,
            current_app.config["DATABASE_BACKEND"],
        )
        return send_file(
            BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="faustos-coffee-productos.pdf",
        )
