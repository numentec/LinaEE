from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "wms"

router = DefaultRouter()
router.register(r'wmsqueries', views.WMSQueryModelViewset, basename='wmsqueries')
router.register(r'wmstools', views.WMSToolsModelViewset, basename='wmstools')

urlpatterns = [
    path('', include(router.urls)),
    path('qrystockext/', views.QryStockExtAPIView.as_view(), name='qrystockext'),
    path('relocatext/', views.RelocateExtAPIView.as_view(), name='relocatext'),
    path('qryoneprod/', views.QryOneProdAPIView.as_view(), name='qryoneprod'),
]
