from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExtOrderMasterViewSet,
    ExtOrderMasterOnlyViewSet,
    ItemImagesAPIView,
    GenerateOrderPDF,
    OrderPDFPreview,
    GenerateOrderCSV,
    SendWelcomeEmail,
    SendOrderPDFEmail,
    SendOrderCSVEmail,
    TaskStatus,
    CategoryBrandListAPIView,
    ProductsAPIView,
)

app_name = "shoppingcart"

router = DefaultRouter()
router.register(r'extorder', ExtOrderMasterViewSet, basename='extorder')
router.register(r'extorderonly', ExtOrderMasterOnlyViewSet, basename='extorderonly')

urlpatterns = [
    path('catsbrands/', CategoryBrandListAPIView.as_view(), name='catsbrands'),
    path('products/', ProductsAPIView.as_view(), name='products'),
    path('itemimages/<str:subfolder>/', ItemImagesAPIView.as_view(), name='itemimages'),
    path('orders/<int:order_id>/preview/', OrderPDFPreview.as_view(), name='order-pdf-preview'),
    path('orders/<int:order_id>/pdf/', GenerateOrderPDF.as_view(), name='order-pdf'),
    path('orders/<int:order_id>/csv/', GenerateOrderCSV.as_view(), name='order-csv'),
    path('orders/<int:order_id>/email-pdf/', SendOrderPDFEmail.as_view(), name='order-email-pdf'),
    path('orders/<int:order_id>/email-csv/', SendOrderCSVEmail.as_view(), name='order-email-csv'),
    path('email-wellcome/', SendWelcomeEmail.as_view(), name='email-wellcome'),
    path('task-status/<taskid>/', TaskStatus.as_view(), name='task-status'),
    path('', include(router.urls)),
]
