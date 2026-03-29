from app.models import Producto


class CatalogService:
    def __init__(self, inventario, file_service):
        self.inventario = inventario
        self.file_service = file_service

    def initialize_catalog(self):
        self.inventario.inicializar_base_datos()
        self.inventario.sembrar_datos_iniciales(self._seed_products())
        self.sync_flat_files()

    def _seed_products(self) -> list[Producto]:
        return [
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

    def list_products(self) -> list[Producto]:
        return self.inventario.listar_productos()

    def get_product_by_id(self, product_id: int) -> Producto | None:
        return self.inventario.obtener_producto_por_id(product_id)

    def get_product_by_slug(self, slug: str) -> Producto | None:
        return self.inventario.obtener_producto_por_slug(slug)

    def create_product(self, product: Producto) -> Producto:
        creado = self.inventario.crear_producto(product)
        self.sync_flat_files()
        return creado

    def update_product(self, product_id: int, product: Producto):
        self.inventario.actualizar_producto(product_id, product)
        self.sync_flat_files()

    def delete_product(self, product_id: int):
        self.inventario.eliminar_producto(product_id)
        self.sync_flat_files()

    def sync_flat_files(self):
        self.file_service.exportar_productos(self.inventario.listar_productos())

    def get_files_report(self) -> dict:
        return self.file_service.obtener_reporte_archivos()
