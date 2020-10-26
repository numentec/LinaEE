from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "core"

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login_refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('cias/', views.CiaList.as_view(), name='cias'),
    path('cias/<pk>', views.CiaDetail.as_view(), name='cia'),
    path('users/', views.UserList.as_view(), name='users'),
    path('users/<pk>', views.UserDetail.as_view(), name='user'),
]