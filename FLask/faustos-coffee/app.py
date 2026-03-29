from flask import Flask, render_template

app = Flask(__name__)

PRODUCTOS = [
    {
        "slug": "espresso-premium",
        "nombre": "Espresso Premium",
        "descripcion": "Tueste intenso con notas de cacao y un final persistente.",
        "precio": "$8.50",
    },
    {
        "slug": "cafe-de-origen",
        "nombre": "Cafe de Origen",
        "descripcion": "Granos seleccionados con aroma floral y acidez equilibrada.",
        "precio": "$10.00",
    },
    {
        "slug": "blend-de-la-casa",
        "nombre": "Blend de la Casa",
        "descripcion": "Mezcla suave para disfrutar en cualquier momento del dia.",
        "precio": "$7.25",
    },
]


@app.route("/")
def home():
    return render_template("index.html", productos=PRODUCTOS)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/productos")
def productos():
    return render_template("productos.html", productos=PRODUCTOS)


@app.route("/producto/<nombre>")
def producto(nombre):
    producto_encontrado = next(
        (producto for producto in PRODUCTOS if producto["slug"] == nombre),
        None,
    )

    if producto_encontrado is None:
        producto_encontrado = {
            "slug": nombre,
            "nombre": nombre.replace("-", " ").title(),
            "descripcion": "Este producto forma parte del catalogo inicial de Faustos Coffee.",
            "precio": "Precio por confirmar",
        }

    return render_template(
        "productos.html",
        productos=PRODUCTOS,
        producto_destacado=producto_encontrado,
    )


if __name__ == "__main__":
    app.run(debug=True)
