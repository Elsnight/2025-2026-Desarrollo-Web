import csv
import json
from pathlib import Path

from app.models import Producto


class FileService:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.txt_path = self.data_dir / "productos.txt"
        self.json_path = self.data_dir / "productos.json"
        self.csv_path = self.data_dir / "productos.csv"

    def exportar_productos(self, productos: list[Producto]):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._exportar_txt(productos)
        self._exportar_json(productos)
        self._exportar_csv(productos)

    def _exportar_txt(self, productos: list[Producto]):
        if not productos:
            contenido = "Faustos Coffee - Productos exportados\n\nNo hay productos registrados.\n"
            self.txt_path.write_text(contenido, encoding="utf-8")
            return

        lineas = ["Faustos Coffee - Productos exportados", ""]

        for indice, producto in enumerate(productos, start=1):
            lineas.extend(
                [
                    f"Producto #{indice}",
                    f"ID: {producto.id}",
                    f"Slug: {producto.slug}",
                    f"Nombre: {producto.nombre}",
                    f"Descripcion: {producto.descripcion}",
                    f"Precio: {producto.precio:.2f}",
                ]
            )
            if indice < len(productos):
                lineas.append("-" * 40)

        self.txt_path.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    def _exportar_json(self, productos: list[Producto]):
        contenido = [self._producto_a_diccionario(producto) for producto in productos]
        self.json_path.write_text(
            json.dumps(contenido, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

    def _exportar_csv(self, productos: list[Producto]):
        with self.csv_path.open("w", newline="", encoding="utf-8") as archivo_csv:
            writer = csv.DictWriter(
                archivo_csv,
                fieldnames=["id", "slug", "nombre", "descripcion", "precio"],
            )
            writer.writeheader()
            writer.writerows(
                [self._producto_a_diccionario(producto) for producto in productos]
            )

    def leer_txt(self) -> str:
        if not self.txt_path.exists():
            return ""
        return self.txt_path.read_text(encoding="utf-8")

    def leer_json(self) -> list[dict]:
        if not self.json_path.exists():
            return []
        return json.loads(self.json_path.read_text(encoding="utf-8"))

    def leer_csv(self) -> list[dict]:
        if not self.csv_path.exists():
            return []

        with self.csv_path.open("r", newline="", encoding="utf-8") as archivo_csv:
            return list(csv.DictReader(archivo_csv))

    def obtener_reporte_archivos(self) -> dict:
        registros_json = self.leer_json()
        return {
            "txt": {
                "ruta": self.txt_path.name,
                "contenido": self.leer_txt(),
            },
            "json": {
                "ruta": self.json_path.name,
                "contenido": json.dumps(registros_json, indent=4, ensure_ascii=False),
                "registros": registros_json,
            },
            "csv": {
                "ruta": self.csv_path.name,
                "registros": self.leer_csv(),
            },
        }

    @staticmethod
    def _producto_a_diccionario(producto: Producto) -> dict:
        return {
            "id": producto.id,
            "slug": producto.slug,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": f"{producto.precio:.2f}",
        }
