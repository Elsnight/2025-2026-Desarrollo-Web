from dataclasses import dataclass

from app.models import Producto


@dataclass(slots=True)
class ProductFormData:
    nombre: str
    descripcion: str
    precio_texto: str
    slug: str

    @classmethod
    def from_mapping(cls, form_data) -> "ProductFormData":
        return cls(
            nombre=form_data.get("nombre", "").strip(),
            descripcion=form_data.get("descripcion", "").strip(),
            precio_texto=form_data.get("precio", "").strip(),
            slug=form_data.get("slug", "").strip(),
        )

    def validate(self) -> list[str]:
        errores = []

        if not self.nombre:
            errores.append("El nombre del producto es obligatorio.")

        if not self.descripcion:
            errores.append("La descripcion del producto es obligatoria.")

        precio = self._parse_price()
        if precio is None or precio <= 0:
            errores.append("El precio debe ser un numero mayor que cero.")

        if not self.slug and not self.nombre:
            errores.append("El slug es obligatorio o debe poder generarse desde el nombre.")

        return errores

    def to_product(self) -> Producto:
        slug = self.slug
        if slug:
            slug = Producto.normalizar_slug(slug)
        else:
            slug = Producto.generar_slug(self.nombre)

        return Producto(
            slug=slug,
            nombre=self.nombre,
            descripcion=self.descripcion,
            precio=self._parse_price(default=0.0),
        )

    def _parse_price(self, default=None):
        try:
            return float(self.precio_texto)
        except ValueError:
            return default


def build_product_from_form(form_data) -> tuple[Producto, list[str]]:
    product_form = ProductFormData.from_mapping(form_data)
    return product_form.to_product(), product_form.validate()
