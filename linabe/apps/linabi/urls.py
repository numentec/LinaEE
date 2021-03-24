from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "linabi"

router = DefaultRouter()
router.register(r'model-catalog', views.CatalogModelViewSet, basename='model-catalog')
router.register(r'favoritos', views.FavoritoModelViewset, basename='favoritos')

urlpatterns = [
    path('', include(router.urls)),
    path('catalog/', views.CatalogAPIView.as_view(), name='catalog'),
    path('saledocsm/', views.SaleDocsMAPIView.as_view(), name='saledocsm'),
    path('saledocsd/', views.SaleDocsDAPIView.as_view(), name='saledocsd'),
]