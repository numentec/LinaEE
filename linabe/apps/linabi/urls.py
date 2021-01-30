from django.urls import path

from . import views

urlpatterns = [
    path('testapi/', views.TestApiView.as_view(), name='testapi'),
]