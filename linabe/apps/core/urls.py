from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('cias/', views.CiaList.as_view(), name='cias'),
    path('cias/<pk>', views.CiaDetail.as_view(), name='cia'),
]