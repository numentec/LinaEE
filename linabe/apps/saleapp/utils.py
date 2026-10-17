# utils.py
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from io import StringIO, BytesIO
from django.conf import settings
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Font, PatternFill
from PIL import Image as PILImage
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
    html_string = render_to_string('saleapp/order_pdf.html', {
        'order': order,
        'order_date': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'items': items,
        'logo_url': logo_url,
        'print_images': print_images,
        'created_by_name': order.created_by.get_full_name(),
        'created_by_email': order.created_by.email,
    }) #.encode('utf-8', errors='replace').decode('utf-8', errors='replace')

    # Crear un objeto BytesIO para almacenar el PDF
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


# Tamaño máximo (px) de las imágenes incrustadas en el Excel
XLSX_IMG_SIZE = (120, 120)


def _xlsx_image(sku):
    """
    Devuelve la foto del sku reducida como imagen de openpyxl,
    o None si no existe o no se puede leer.
    """
    path = os.path.join(settings.MEDIA_ROOT, 'fotos', f'{sku}.jpg')

    if not os.path.isfile(path):
        return None

    try:
        with PILImage.open(path) as img:
            img = img.convert('RGB')
            img.thumbnail(XLSX_IMG_SIZE)
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        return XLImage(buffer)
    except Exception:
        return None


def render_order_xlsx(order, print_images=True):
    wb = Workbook()
    ws = wb.active
    ws.title = f'Order {order.id}'

    bold = Font(bold=True)
    header_fill = PatternFill('solid', fgColor='A6EFFE')
    money = '#,##0.00'

    # Encabezado de la orden
    created_by = order.created_by
    info = [
        ('Order #', order.id),
        ('Date', order.created_at.strftime('%Y-%m-%d %H:%M:%S')),
        ('Customer', f'{order.customer_id} {order.customer_name or ""}'.strip()),
        ('e-mail', order.sendto),
        ('Phone', order.customer_cel),
        ('Seller', created_by.get_full_name() if created_by else ''),
        ('Status', order.get_status_display()),
    ]
    for label, value in info:
        ws.append([label, value])
        ws.cell(row=ws.max_row, column=1).font = bold

    ws.append([])

    # Tabla de items
    columns = ['Image', 'SKU', 'Description', 'Qty', 'Price', 'Amount']
    if not print_images:
        columns = columns[1:]

    ws.append(columns)
    header_row = ws.max_row
    for cell in ws[header_row]:
        cell.font = bold
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')

    offset = 1 if print_images else 0
    first_row = header_row + 1

    for item in order.items.all():
        values = [item.sku, item.name, item.quantity, item.price,
                  round(item.quantity * item.price, 2)]
        ws.append([None] * offset + values)
        row = ws.max_row

        for col in range(1, len(columns) + 1):
            ws.cell(row=row, column=col).alignment = Alignment(vertical='center', wrap_text=True)
        ws.cell(row=row, column=offset + 4).number_format = money
        ws.cell(row=row, column=offset + 5).number_format = money

        if print_images:
            img = _xlsx_image(item.sku)
            if img:
                ws.add_image(img, f'A{row}')
                # Alto de fila en puntos (1px ≈ 0.75pt)
                ws.row_dimensions[row].height = img.height * 0.75 + 4

    last_row = ws.max_row

    # Total
    ws.append([])
    ws.append([None] * (offset + 3) + ['Total', order.total])
    total_row = ws.max_row
    ws.cell(row=total_row, column=offset + 4).font = bold
    ws.cell(row=total_row, column=offset + 5).font = bold
    ws.cell(row=total_row, column=offset + 5).number_format = money

    # Formato de hoja
    widths = [18, 45, 8, 12, 14]
    if print_images:
        widths = [XLSX_IMG_SIZE[0] / 7 + 2] + widths  # ancho en caracteres (~7px c/u)
    for idx, width in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + idx)].width = width

    ws.freeze_panes = f'A{first_row}'
    if last_row >= first_row:
        ws.auto_filter.ref = f'A{header_row}:{chr(64 + len(columns))}{last_row}'

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file
