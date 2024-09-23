from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "linabi"

router = DefaultRouter()
router.register(r'model-catalog', views.CatalogModelViewSet, basename='model-catalog')
router.register(r'biqueries', views.BIQueryModelViewset, basename='biqueries')
router.register(r'favoritos', views.FavoritoModelViewset, basename='favoritos')
router.register(r'xlsxtemplates', views.BIXLSXTemplateModelViewset, basename='xlsxtemplates')
router.register(r'xlsxtemplatescols', views.BIXLSXTemplateColModelViewset, basename='xlsxtemplatescols')

urlpatterns = [
    path('', include(router.urls)),
    path('catalog/', views.CatalogAPIView.as_view(), name='catalog'),
    path('saledocsm/', views.SaleDocsMAPIView.as_view(), name='saledocsm'),
    path('saledocsd/', views.SaleDocsDAPIView.as_view(), name='saledocsd'),
    path('salesdetail/', views.SalesDetailAPIView.as_view(), name='salesdetail'),
    path('storagexloc/', views.StoragexlocAPIView.as_view(), name='storagexloc'),
    path('clists/', views.CommonListsAPIView.as_view(), name='commonlists'),
    path('tallasbc/', views.TallasBCAPIView.as_view(), name='tallasbc'),
    path('coloresbc/', views.ColoresBCAPIView.as_view(), name='coloresbc'),
    path('extbidashboard/', views.BIDashboardExt.as_view(), name='extbidashboard'),
    path('cxcantig/', views.CxCAntigAPIView.as_view(), name='cxcantig'),
]
