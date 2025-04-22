from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ExtOrderMasterViewSet, ExtOrderMasterOnlyViewSet, ItemImagesAPIView, GenerateOrderPDF, GenerateOrderCSV

app_name = "shoppingcart"

router = DefaultRouter()
router.register(r'extorder', ExtOrderMasterViewSet, basename='extorder')
router.register(r'extorderonly', ExtOrderMasterOnlyViewSet, basename='extorderonly')

urlpatterns = [
    path('catsbrands/', views.CategoryBrandListAPIView.as_view(), name='catsbrands'),
    path('products/', views.ProductsAPIView.as_view(), name='products'),
    path('itemimages/<str:subfolder>/', ItemImagesAPIView.as_view(), name='itemimages'),
    path('orders/<int:order_id>/pdf/', GenerateOrderPDF.as_view(), name='order-pdf'),
    path('orders/<int:order_id>/csv/', GenerateOrderCSV.as_view(), name='order-csv'),
    path('', include(router.urls)),
]
