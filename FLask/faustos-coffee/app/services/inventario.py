from app.models import Producto
from app.extensions import db
from sqlalchemy.exc import IntegrityError, OperationalError


class Inventario:
    def inicializar_base_datos(self):
        try:
            db.create_all()
        except OperationalError as error:
            raise RuntimeError(
                "No se pudo conectar a la base de datos configurada. "
                "Verifica que MySQL este encendido y que las variables de entorno sean correctas."
            ) from error

    def sembrar_datos_iniciales(self, productos: list[Producto]):
        if self.contar_productos() > 0:
            return

        db.session.add_all(productos)
        db.session.commit()

    def contar_productos(self) -> int:
        consulta = db.select(db.func.count()).select_from(Producto)
        return db.session.scalar(consulta) or 0

    def listar_productos(self) -> list[Producto]:
        consulta = db.select(Producto).order_by(Producto.id.asc())
        return db.session.execute(consulta).scalars().all()

    def obtener_producto_por_id(self, producto_id: int) -> Producto | None:
        return db.session.get(Producto, producto_id)

    def obtener_producto_por_slug(self, slug: str) -> Producto | None:
        consulta = db.select(Producto).where(Producto.slug == slug)
        return db.session.execute(consulta).scalar_one_or_none()

    def crear_producto(self, producto: Producto) -> Producto:
        try:
            db.session.add(producto)
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            raise ValueError(
                "Ya existe un producto con ese slug. Usa un slug diferente."
            ) from error

        return producto

    def actualizar_producto(self, producto_id: int, producto: Producto):
        producto_existente = self.obtener_producto_por_id(producto_id)
        if producto_existente is None:
            raise ValueError("No se encontro el producto a actualizar.")

        producto_existente.slug = producto.slug
        producto_existente.nombre = producto.nombre
        producto_existente.descripcion = producto.descripcion
        producto_existente.precio = producto.precio

        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            raise ValueError(
                "No se pudo actualizar el producto porque el slug ya existe."
            ) from error

    def eliminar_producto(self, producto_id: int):
        producto_existente = self.obtener_producto_por_id(producto_id)
        if producto_existente is None:
            raise ValueError("No se encontro el producto a eliminar.")

        db.session.delete(producto_existente)
        db.session.commit()
