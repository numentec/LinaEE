# import json
# import random

# import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from celery.signals import task_postrun
from .consumers import notify_channel_layer
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

from .models import ExtOrderMaster
from .utils import render_order_pdf, render_order_csv


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
def send_order_email(order_id, print_images='', file_type='pdf'):
    """
    Tarea de Celery para enviar un correo electrónico con los detalles de la orden.
    Esta tarea se ejecuta en segundo plano y genera un PDF y un CSV de la orden,
    luego envía un correo electrónico al cliente con los archivos adjuntos.
    """
    try:
        # Obtener la orden
        order = ExtOrderMaster.objects.get(id=order_id)

        # Crear el correo electrónico
        email = EmailMessage(
            subject=f"Order #{order.id} Details",
            body=f"Dear {order.customer_name},\n\nPlease find attached the details of your order #{order.id}.",
            from_email="no-reply@numen.pa",
            to=[order.sendto],
        )

        # Generar el PDF o el CSV
        if file_type == 'pdf':
            pdf_file = render_order_pdf(order, print_images=print_images)
            email.attach(f"Order_{order.id}.pdf", pdf_file.getvalue(), "application/pdf")
        elif file_type == 'csv':
            csv_file = render_order_csv(order)
            email.attach(f"Order_{order.id}.csv", csv_file.getvalue(), "text/csv")
        else:
            raise ValueError("Invalid file type specified. Use 'pdf' or 'csv'.")

        # Enviar el correo
        email.send()
        return f"Email sent successfully for order #{order.id}"
    except ExtOrderMaster.DoesNotExist:
        return f"Order with ID {order_id} does not exist"
    except Exception as e:
        return f"Error sending email for order #{order_id}: {str(e)}"