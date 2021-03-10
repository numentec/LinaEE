from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "linabi"

router = DefaultRouter()
# router.register(r'catalog', views.CatalogModelViewSet, basename='catalog')
router.register(r'favoritos', views.FavoritoModelViewset, basename='favoritos')

urlpatterns = [
    path('', include(router.urls)),
    path('catalog/', views.CatalogAPIView.as_view(), name='catalog'),
]