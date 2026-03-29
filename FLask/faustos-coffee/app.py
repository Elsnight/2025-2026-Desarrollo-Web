from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

from models.producto import Producto
from services.inventario import Inventario

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "faustos_coffee.sqlite3"

app = Flask(__name__)
app.config["SECRET_KEY"] = "faustos-coffee-dev"

inventario = Inventario(DB_PATH)


def inicializar_inventario():
    inventario.inicializar_base_datos()
    inventario.sembrar_datos_iniciales(
        [
            Producto(
                slug="espresso-premium",
                nombre="Espresso Premium",
                descripcion="Tueste intenso con notas de cacao y un final persistente.",
                precio=8.50,
            ),
            Producto(
                slug="cafe-de-origen",
                nombre="Cafe de Origen",
                descripcion="Granos seleccionados con aroma floral y acidez equilibrada.",
                precio=10.00,
            ),
            Producto(
                slug="blend-de-la-casa",
                nombre="Blend de la Casa",
                descripcion="Mezcla suave para disfrutar en cualquier momento del dia.",
                precio=7.25,
            ),
        ]
    )


def construir_producto_desde_formulario(formulario):
    nombre = formulario.get("nombre", "").strip()
    descripcion = formulario.get("descripcion", "").strip()
    precio_texto = formulario.get("precio", "").strip()
    slug = formulario.get("slug", "").strip()
    errores = []

    if not nombre:
        errores.append("El nombre del producto es obligatorio.")

    if not descripcion:
        errores.append("La descripcion del producto es obligatoria.")

    try:
        precio = float(precio_texto)
        if precio <= 0:
            raise ValueError
    except ValueError:
        errores.append("El precio debe ser un numero mayor que cero.")
        precio = 0.0

    if slug:
        slug = Producto.normalizar_slug(slug)
    elif nombre:
        slug = Producto.generar_slug(nombre)

    if not slug:
        errores.append("El slug es obligatorio o debe poder generarse desde el nombre.")

    return (
        Producto(
            slug=slug,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
        ),
        errores,
    )


inicializar_inventario()


@app.route("/")
def home():
    productos = inventario.listar_productos()
    producto_destacado = productos[0] if productos else None
    return render_template(
        "index.html",
        productos=productos,
        producto_destacado=producto_destacado,
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/productos")
def productos():
    return render_template(
        "productos.html",
        productos=inventario.listar_productos(),
        producto_destacado=None,
    )


@app.route("/producto/<slug>")
def producto(slug):
    producto_encontrado = inventario.obtener_producto_por_slug(slug)

    if producto_encontrado is None:
        flash("El producto solicitado no existe en el inventario actual.", "warning")
        return redirect(url_for("productos"))

    return render_template(
        "productos.html",
        productos=inventario.listar_productos(),
        producto_destacado=producto_encontrado,
    )


@app.route("/admin/productos")
def admin_productos():
    producto_id = request.args.get("editar", type=int)
    producto_editar = None

    if producto_id is not None:
        producto_editar = inventario.obtener_producto_por_id(producto_id)
        if producto_editar is None:
            flash("El producto que intentas editar no existe.", "warning")
            return redirect(url_for("admin_productos"))

    return render_template(
        "admin_productos.html",
        productos=inventario.listar_productos(),
        producto_editar=producto_editar,
    )


@app.post("/admin/productos/crear")
def crear_producto():
    producto, errores = construir_producto_desde_formulario(request.form)

    if errores:
        for error in errores:
            flash(error, "danger")
        return redirect(url_for("admin_productos"))

    try:
        inventario.crear_producto(producto)
    except ValueError as error:
        flash(str(error), "danger")
        return redirect(url_for("admin_productos"))

    flash("Producto creado correctamente en SQLite.", "success")
    return redirect(url_for("admin_productos"))


@app.post("/admin/productos/<int:producto_id>/editar")
def editar_producto(producto_id):
    producto_existente = inventario.obtener_producto_por_id(producto_id)

    if producto_existente is None:
        flash("El producto a editar no fue encontrado.", "warning")
        return redirect(url_for("admin_productos"))

    producto, errores = construir_producto_desde_formulario(request.form)

    if errores:
        for error in errores:
            flash(error, "danger")
        return redirect(url_for("admin_productos", editar=producto_id))

    try:
        inventario.actualizar_producto(producto_id, producto)
    except ValueError as error:
        flash(str(error), "danger")
        return redirect(url_for("admin_productos", editar=producto_id))

    flash("Producto actualizado correctamente.", "success")
    return redirect(url_for("admin_productos"))


@app.post("/admin/productos/<int:producto_id>/eliminar")
def eliminar_producto(producto_id):
    producto_existente = inventario.obtener_producto_por_id(producto_id)

    if producto_existente is None:
        flash("El producto a eliminar no existe.", "warning")
        return redirect(url_for("admin_productos"))

    inventario.eliminar_producto(producto_id)
    flash("Producto eliminado del inventario.", "success")
    return redirect(url_for("admin_productos"))


if __name__ == "__main__":
    app.run(debug=True)
