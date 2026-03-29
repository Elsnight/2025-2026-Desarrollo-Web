import re

from app.extensions import db


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), nullable=False, unique=True, index=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    @property
    def precio_formateado(self) -> str:
        return f"${self.precio:.2f}"

    @staticmethod
    def normalizar_slug(texto: str) -> str:
        slug = texto.strip().lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        return slug.strip("-")

    @classmethod
    def generar_slug(cls, nombre: str) -> str:
        return cls.normalizar_slug(nombre)
