from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "core"

router = DefaultRouter()
router.register('cias', views.CiaViewSet)

urlpatterns = [
    path('login/', views.LinaAuthToken.as_view(), name='login'),
    path('loginjwt/', TokenObtainPairView.as_view(), name='loginjwt'),
    path('loginjwt_refresh/', TokenRefreshView.as_view(), name='loginjwt_refresh'),
    path('', include(router.urls)),
    # path('cias/', views.CiaList.as_view(), name='cias'),
    # path('cias/<pk>/', views.CiaDetail.as_view(), name='cia'),
    # path('cia/create/', views.CiaCreate.as_view(), name='cia_create'),
    path('users/<username>/', views.UserList.as_view(), name='users'),
    path('users/<pk>/', views.UserDetail.as_view(), name='user'),
    path('user_perms/<pk>/', views.UserPermsDetail.as_view(), name='user_perms'),
    path('user_register/', views.UserRegister.as_view(), name='user_register'),
    path('groups/', views.GroupsList.as_view(), name='groups'),
]