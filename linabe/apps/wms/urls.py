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
    path('qrybasestockext/', views.QryBaseStockExtAPIView.as_view(), name='qrybasestockext'),
    path('relocatext/', views.RelocateExtAPIView.as_view(), name='relocatext'),
    path('qryoneprod/', views.QryOneProdAPIView.as_view(), name='qryoneprod'),
    path('prodsperloc/', views.ProdsPerLocAPIView.as_view(), name='prodsperloc'),
    path('extmarbete/', views.ProdsPerMarbeteAPIView.as_view(), name='extmarbete'),
    path('extcountedprods/', views.ExtCountedProdsAPIView.as_view(), name='extcountedprods'),
]
