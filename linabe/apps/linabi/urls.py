from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "linabi"

router = DefaultRouter()
router.register(r'catalog', views.CatalogModelViewSet, basename='catalog')

urlpatterns = [
    path('', include(router.urls)),
]