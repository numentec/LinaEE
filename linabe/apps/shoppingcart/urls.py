from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "shoppingcart"

urlpatterns = [
    path('catsbrands/', views.CategoryBrandListAPIView.as_view(), name='catsbrands'),
]
