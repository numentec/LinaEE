# import json
# import random

# import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from celery.signals import task_postrun
from .consumers import notify_channel_layer
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

from apps.core.models import EmailSettings
from .models import ExtOrderMaster
from .utils import render_order_pdf, render_order_csv, render_order_xlsx


LinaUserModel = get_user_model()

logger = get_task_logger(__name__)


@shared_task(name='high_priority:task_send_welcome_email')
def task_send_welcome_email(user_pk):
    user = LinaUserModel.objects.get(pk=user_pk)
    logger.info(f'send email to {user.email} {user.pk}')


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    """
    When celery task finish, send notification to Django channel_layer, so Django channel would receive
    the event and then send it to web client
    """
    notify_channel_layer(task_id)


@shared_task(name='high_priority:send_order_email')
def send_order_email(order_id, print_images='', file_type='pdf', file_types=None, to=None,
                     user_email=None):
    """
    Tarea de Celery para enviar un correo electrónico con los detalles de la orden.
    Esta tarea se ejecuta en segundo plano, genera los archivos de la orden
    (file_types, p.ej. ['pdf', 'xlsx'], o solo file_type) y los envía
    adjuntos en un único correo a los destinatarios indicados (to)
    o, si no se indican, al sendto de la orden.
    user_email: correo del usuario que solicita el envío (Responder a, según EmailSettings).
    """
    file_types = list(file_types or [file_type])
    try:
        # Obtener la orden
        order = ExtOrderMaster.objects.get(id=order_id)

        # Crear el correo electrónico
        email = EmailMessage(
            subject=f"Order #{order.id} Details",
            body=f"Dear {order.customer_name},\n\nPlease find attached the details of your order #{order.id}.",
            to=list(to or [order.sendto]),
            reply_to=EmailSettings.load().reply_to_for(user_email),
        )

        # Generar los archivos según los tipos solicitados
        renderers = {
            'pdf': (lambda: render_order_pdf(order, print_images=print_images), "application/pdf"),
            'csv': (lambda: render_order_csv(order), "text/csv"),
            'xlsx': (
                lambda: render_order_xlsx(order, print_images=print_images != '0'),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
        }
        invalid = [t for t in file_types if t not in renderers]
        if invalid:
            raise ValueError(f"Invalid file type specified. Use one of: {', '.join(renderers)}.")

        for ftype in file_types:
            render, mimetype = renderers[ftype]
            email.attach(f"Order_{order.id}.{ftype}", render().getvalue(), mimetype)

        # Enviar el correo
        email.send()
        return f"Email sent successfully for order #{order.id}"
    except ExtOrderMaster.DoesNotExist:
        return f"Order with ID {order_id} does not exist"
    except Exception as e:
        return f"Error sending email for order #{order_id}: {str(e)}"