from dataclasses import dataclass
import re


@dataclass(slots=True)
class Producto:
    id: int | None = None
    slug: str = ""
    nombre: str = ""
    descripcion: str = ""
    precio: float = 0.0

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

    @classmethod
    def desde_fila(cls, fila) -> "Producto":
        return cls(
            id=fila["id"],
            slug=fila["slug"],
            nombre=fila["nombre"],
            descripcion=fila["descripcion"],
            precio=fila["precio"],
        )
