# import json
# import random

# import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from celery.signals import task_postrun
from .consumers import notify_channel_layer
from django.contrib.auth import get_user_model


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