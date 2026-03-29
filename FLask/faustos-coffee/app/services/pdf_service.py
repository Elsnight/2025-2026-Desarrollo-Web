from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class ProductReportService:
    def build_products_pdf(self, productos, database_backend: str) -> bytes:
        buffer = BytesIO()
        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
            title="Reporte de productos - Faustos Coffee",
            author="Faustos Coffee",
        )

        styles = getSampleStyleSheet()
        body_style = styles["BodyText"]
        body_style.spaceAfter = 0
        body_style.leading = 14
        product_style = ParagraphStyle(
            "ProductCell",
            parent=body_style,
            fontSize=9,
            leading=12,
        )

        total_catalogo = sum(producto.precio for producto in productos)
        generated_at = datetime.now().strftime("%d/%m/%Y %H:%M")

        elements = [
            Paragraph("Faustos Coffee", styles["Title"]),
            Spacer(1, 0.2 * cm),
            Paragraph(
                "Reporte academico del catalogo de productos generado desde la aplicacion web.",
                body_style,
            ),
            Spacer(1, 0.5 * cm),
        ]

        resumen = Table(
            [
                ["Fecha de generacion", generated_at],
                ["Motor de base de datos", database_backend],
                ["Total de productos", str(len(productos))],
                ["Valor total del catalogo", f"${total_catalogo:.2f}"],
            ],
            colWidths=[6 * cm, 10 * cm],
            hAlign="LEFT",
        )
        resumen.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1e4d5")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#2f241f")),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8c3ad")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        elements.extend([resumen, Spacer(1, 0.6 * cm)])

        table_data = [["ID", "Producto", "Slug", "Precio"]]
        for producto in productos:
            detalle_producto = Paragraph(
                f"<b>{producto.nombre}</b><br/>{producto.descripcion}",
                product_style,
            )
            table_data.append(
                [
                    str(producto.id or "-"),
                    detalle_producto,
                    producto.slug,
                    producto.precio_formateado,
                ]
            )

        tabla_productos = Table(
            table_data,
            colWidths=[1.5 * cm, 8.8 * cm, 4.3 * cm, 2.4 * cm],
            repeatRows=1,
            hAlign="LEFT",
        )
        tabla_productos.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6f4e37")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("LEADING", (0, 1), (-1, -1), 12),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8c3ad")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#faf4ee")]),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        elements.append(tabla_productos)

        document.build(elements)
        return buffer.getvalue()
