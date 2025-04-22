# utils.py
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from django.conf import settings
import os

def render_order_pdf(order):
    logo_path = os.path.join(settings.STATIC_ROOT, "images", "logo.png")
    logo_url = f"file://{logo_path}"

    items = []

    for item in order.items.all():
        item.line_total = round(item.quantity * item.price, 2)

        items.append(item)

    # Renderizar la plantilla HTML con los datos de la orden
    html_string = render_to_string('shoppingcart/order_pdf.html', {
        'order': order,
        'logo_url': logo_url,
        'items': items,
    })

    pdf_file = BytesIO()

    # Generar el PDF a partir del HTML utilizando WeasyPrint
    # WeasyPrint requiere que el HTML esté en formato UTF-8
    # y que se especifique el encoding al escribir el PDF
    HTML(string=html_string).write_pdf(target=pdf_file)
    pdf_file.seek(0)
    return pdf_file
