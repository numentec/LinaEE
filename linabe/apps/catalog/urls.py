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
    CategoriesListAPIView,
    TopCategoriesByCompanyAPIView,
    CategoriesByParentAndCompanyAPIView,
    CatalogDetailView,
    PublicCatalogByTokenView,
    MockProductsAPIView,
)
from .api_pdf_jobs import pdf_job_status, pdf_job_download
app_name = "catalog"

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'api/catalogs', CatalogViewSet, basename='catalogs')
router.register(r'catalogsonly', CatalogMasterViewSet, basename='catalogsonly') # Devuelve solo el maestro del catálogo
router.register(r'catalog-details', CatalogDetailViewSet, basename='catalog-details') # Devuelve detalles del catálogo
router.register(r'catalog-detail-images', CatalogDetailImageViewSet, basename='catalog-detail-images') # Devuelve imágenes de detalles del catálogo

urlpatterns = [
    # Devuelve los catálogos activos de un cliente
    # Se usa el ulid del cliente para filtrar los catálogos activos
    # y el token para validar el acceso a un catálogo específico
    path('by-customer/<str:ulid>/', ActiveCustomerCatalogsAPIView.as_view(), name='active-customer-catalogs'),
    path('by-customer/<str:ulid>/<str:token>/', ValidCustomerCatalogAPIView.as_view(), name='valid-customer-catalog'),

    path("api/catalogos/<int:pk>/", CatalogDetailView.as_view()),
    path("api/public/catalogos/<str:token>/", PublicCatalogByTokenView.as_view()),
    path("api/pdf-jobs/<str:job_id>/", pdf_job_status),
    path("api/pdf-jobs/<str:job_id>/download/", pdf_job_download),

    # Endpoints para consultas de categorías
    # 1. Listado general de todas las categorías con compañías disponibles
    path('categories/list/', CategoriesListAPIView.as_view(), name='categories-list'),
    
    # 2. Categorías padre (top fathers) para una compañía específica
    path('categories/top-by-company/<int:company_id>/', TopCategoriesByCompanyAPIView.as_view(), name='top-categories-by-company'),
    
    # 3. Subcategorías de un padre específico para una compañía
    path('categories/by-parent/<int:company_id>/<int:parent_id>/', CategoriesByParentAndCompanyAPIView.as_view(), name='categories-by-parent-and-company'),
    
    # Endpoint para mock de productos (solo para pruebas, no debe usarse en producción)
    path('mock/productos/', MockProductsAPIView.as_view(), name='mock-productos'),
    
    path('', include(router.urls)),
]
