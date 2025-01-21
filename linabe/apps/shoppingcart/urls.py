from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ExtOrderMasterViewSet, ExtOrderMasterOnlyViewSet

app_name = "shoppingcart"

router = DefaultRouter()
router.register(r'extorder', ExtOrderMasterViewSet, basename='extorder')
router.register(r'extorderonly', ExtOrderMasterOnlyViewSet, basename='extorderonly')

urlpatterns = [
    path('catsbrands/', views.CategoryBrandListAPIView.as_view(), name='catsbrands'),
    path('products/', views.ProductsAPIView.as_view(), name='products'),
    path('', include(router.urls)),
]
