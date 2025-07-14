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
router.register(r'catalogs', CatalogViewSet, basename='catalogs')
router.register(r'catalogsonly', CatalogMasterViewSet, basename='catalogsonly')
router.register(r'catalog-details', CatalogDetailViewSet, basename='catalog-details')
router.register(r'catalog-detail-images', CatalogDetailImageViewSet, basename='catalog-detail-images')

urlpatterns = [
    path('by-customer/<str:ulid>/', ActiveCustomerCatalogsAPIView.as_view(), name='active-customer-catalogs'),
    path('by-customer/<str:ulid>/<str:token>/', ValidCustomerCatalogAPIView.as_view(), name='valid-customer-catalog'),
    path('', include(router.urls)),
]
