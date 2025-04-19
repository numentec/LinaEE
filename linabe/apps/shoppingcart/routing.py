from django.urls import path

from .consumers import TaskStatusConsumer


urlpatterns = [
    path('ws/task_status/<task_id>/', TaskStatusConsumer.as_asgi()),
]
