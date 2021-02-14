from django.urls import path

from . import views

urlpatterns = [
    path('testapi/', views.TestApiView.as_view(), name='testapi'),
    path('testapi2/', views.TestApiView2.as_view(), name='testapi2'),
]