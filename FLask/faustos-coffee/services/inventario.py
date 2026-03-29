from pathlib import Path
import sqlite3

from models.producto import Producto


class Inventario:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)

    def _conectar(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conexion = sqlite3.connect(self.db_path)
        conexion.row_factory = sqlite3.Row
        return conexion

    def inicializar_base_datos(self):
        with self._conectar() as conexion:
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT NOT NULL UNIQUE,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    precio REAL NOT NULL CHECK (precio > 0)
                )
                """
            )
            conexion.commit()

    def sembrar_datos_iniciales(self, productos: list[Producto]):
        if self.contar_productos() > 0:
            return

        with self._conectar() as conexion:
            conexion.executemany(
                """
                INSERT INTO productos (slug, nombre, descripcion, precio)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (
                        producto.slug,
                        producto.nombre,
                        producto.descripcion,
                        producto.precio,
                    )
                    for producto in productos
                ],
            )
            conexion.commit()

    def contar_productos(self) -> int:
        with self._conectar() as conexion:
            fila = conexion.execute("SELECT COUNT(*) AS total FROM productos").fetchone()
        return fila["total"]

    def listar_productos(self) -> list[Producto]:
        with self._conectar() as conexion:
            filas = conexion.execute(
                """
                SELECT id, slug, nombre, descripcion, precio
                FROM productos
                ORDER BY id ASC
                """
            ).fetchall()
        return [Producto.desde_fila(fila) for fila in filas]

    def obtener_producto_por_id(self, producto_id: int) -> Producto | None:
        with self._conectar() as conexion:
            fila = conexion.execute(
                """
                SELECT id, slug, nombre, descripcion, precio
                FROM productos
                WHERE id = ?
                """,
                (producto_id,),
            ).fetchone()
        return Producto.desde_fila(fila) if fila else None

    def obtener_producto_por_slug(self, slug: str) -> Producto | None:
        with self._conectar() as conexion:
            fila = conexion.execute(
                """
                SELECT id, slug, nombre, descripcion, precio
                FROM productos
                WHERE slug = ?
                """,
                (slug,),
            ).fetchone()
        return Producto.desde_fila(fila) if fila else None

    def crear_producto(self, producto: Producto) -> Producto:
        try:
            with self._conectar() as conexion:
                cursor = conexion.execute(
                    """
                    INSERT INTO productos (slug, nombre, descripcion, precio)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        producto.slug,
                        producto.nombre,
                        producto.descripcion,
                        producto.precio,
                    ),
                )
                conexion.commit()
        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Ya existe un producto con ese slug. Usa un slug diferente."
            ) from error

        return Producto(
            id=cursor.lastrowid,
            slug=producto.slug,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=producto.precio,
        )

    def actualizar_producto(self, producto_id: int, producto: Producto):
        try:
            with self._conectar() as conexion:
                cursor = conexion.execute(
                    """
                    UPDATE productos
                    SET slug = ?, nombre = ?, descripcion = ?, precio = ?
                    WHERE id = ?
                    """,
                    (
                        producto.slug,
                        producto.nombre,
                        producto.descripcion,
                        producto.precio,
                        producto_id,
                    ),
                )
                conexion.commit()
        except sqlite3.IntegrityError as error:
            raise ValueError(
                "No se pudo actualizar el producto porque el slug ya existe."
            ) from error

        if cursor.rowcount == 0:
            raise ValueError("No se encontro el producto a actualizar.")

    def eliminar_producto(self, producto_id: int):
        with self._conectar() as conexion:
            conexion.execute(
                "DELETE FROM productos WHERE id = ?",
                (producto_id,),
            )
            conexion.commit()
