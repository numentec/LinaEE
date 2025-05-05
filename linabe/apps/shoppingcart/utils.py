# utils.py
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from io import StringIO, BytesIO
from django.conf import settings
import os
import csv

def render_order_pdf(order, print_images=''):
    logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'images', 'logo.png')
    logo_url = f'file://{logo_path}'

    # print('***** ORDER ****')
    # for attr, value in vars(order).items():
    #     print(f'{attr}: {value}')

    if print_images == '1':
        print_images = os.path.join(settings.MEDIA_ROOT, 'fotos')
        print_images = f'file://{print_images}'

    styles = CSS(settings.STATICFILES_DIRS[0] + '/css/bootstrap.min.css')

    items = []

    for item in order.items.all():
        item.line_total = round(item.quantity * item.price, 2)

        items.append(item)

    # Renderizar la plantilla HTML con los datos de la orden
    html_string = render_to_string('shoppingcart/order_pdf.html', {
        'order': order,
        'order_date': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'items': items,
        'logo_url': logo_url,
        'print_images': print_images,
        'created_by_name': order.created_by.get_full_name(),
        'created_by_email': order.created_by.email,
    }) #.encode('utf-8', errors='replace').decode('utf-8', errors='replace')

    pdf_file = BytesIO()

    # Generar el PDF a partir del HTML utilizando WeasyPrint
    # WeasyPrint requiere que el HTML esté en formato UTF-8
    # y que se especifique el encoding al escribir el PDF
    HTML(string=html_string).write_pdf(target=pdf_file, stylesheets=[styles])
    pdf_file.seek(0)
    return pdf_file


def render_order_csv(order, mode="short"):
    buffer = StringIO()
    writer = csv.writer(buffer)

    if mode == "full":
        # Cabecera completa
        writer.writerow(['ORDERID', 'DATE', 'SKU', 'Description', 'Quantity', 'Price', 'Amount'])

        # Filas completas
        for item in order.items.all():
            writer.writerow([
                order.id,
                order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                item.sku,
                item.name,
                item.quantity,
                item.price,
                round(item.quantity * item.price, 2)
            ])

        # Opcional: resumen final
        writer.writerow([])
        writer.writerow(['Total', '', '', '', '', '', order.total])
    else:
        # Cabecera reducida
        # writer.writerow(['SKU', 'Quantity', 'Price'])

        # Filas reducidas
        for item in order.items.all():
            writer.writerow([
                item.sku,
                item.quantity,
                item.price
            ])

    # Convertir a BytesIO para descargar o enviar por email
    csv_bytes = BytesIO(buffer.getvalue().encode('utf-8'))
    buffer.close()
    csv_bytes.seek(0)
    return csv_bytes
