from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Faustos Coffee</h1>
    <p>Bienvenido a la tienda online de cafe artesanal.</p>
    <p>Explora nuestros productos y descubre sabores unicos.</p>
    <a href="/producto/espresso-premium">Ver producto destacado</a>
    """


@app.route("/producto/<nombre>")
def producto(nombre):
    nombre_formateado = nombre.replace("-", " ").title()
    return f"""
    <h1>Producto: {nombre_formateado}</h1>
    <p>Este cafe forma parte del catalogo inicial de Faustos Coffee.</p>
    <p>Ideal para la primera fase del proyecto Flask.</p>
    <a href="/">Volver al inicio</a>
    """


if __name__ == "__main__":
    app.run(debug=True)
