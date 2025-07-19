from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    TagViewSet,
    CatalogMasterViewSet,
    CatalogDetailViewSet,
    CatalogDetailImageViewSet,
    CatalogViewSet,
    ActiveCustomerCatalogsAPIView,
    ValidCustomerCatalogAPIView,
)

app_name = "catalog"

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'catalogs', CatalogViewSet, basename='catalogs') # Devuelve Master y detalles del catálogo
router.register(r'catalogsonly', CatalogMasterViewSet, basename='catalogsonly') # Devuelve solo el maestro del catálogo
router.register(r'catalog-details', CatalogDetailViewSet, basename='catalog-details') # Devuelve detalles del catálogo
router.register(r'catalog-detail-images', CatalogDetailImageViewSet, basename='catalog-detail-images') # Devuelve imágenes de detalles del catálogo

urlpatterns = [
    # Devuelve los catálogos activos de un cliente
    # Se usa el ulid del cliente para filtrar los catálogos activos
    # y el token para validar el acceso a un catálogo específico
    path('by-customer/<str:ulid>/', ActiveCustomerCatalogsAPIView.as_view(), name='active-customer-catalogs'),
    path('by-customer/<str:ulid>/<str:token>/', ValidCustomerCatalogAPIView.as_view(), name='valid-customer-catalog'),
    path('', include(router.urls)),
]
