from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "core"

router = DefaultRouter()
router.register(r'cias', views.CiaViewSet, basename='cias')
router.register(r'stakeholders', views.StakeHolderViewSet, basename='stakeholders')
router.register(r'modulos', views.ModuloViewSet, basename='modulos')
router.register(r'vistas', views.VistaViewSet, basename='vistas')
router.register(r'vistas-conf', views.VistaConfigViewSet, basename='vistas-conf')
router.register(r'vistas-conf-usr', views.VistaConfigUserViewSet, basename='vistas-conf-usr')
router.register(r'vistaconfacc', views.VistaConfigAccViewSet, basename='vistaconfacc')
router.register(r'profiles', views.ProfileViewSet, basename='profiles')
router.register(r'sqlqueries', views.SQLQueryViewSet, basename='sqlqueries')

urlpatterns = [
    path('login/', views.LinaAuthToken.as_view(), name='login'),
    path('loginjwt/', TokenObtainPairView.as_view(), name='loginjwt'),
    path('loginjwt_refresh/', TokenRefreshView.as_view(), name='loginjwt_refresh'),
    path('', include(router.urls)),
    # path('cias/', views.CiaList.as_view(), name='cias'),
    # path('cias/<pk>/', views.CiaDetail.as_view(), name='cia'),
    # path('cia/create/', views.CiaCreate.as_view(), name='cia_create'),
    path('users/<username>/', views.UserList.as_view(), name='users'),
    path('user/<pk>/', views.UserDetail.as_view(), name='user'),
    path('user_perms/<pk>/', views.UserPermsDetail.as_view(), name='user_perms'),
    path('user_register/', views.UserRegister.as_view(), name='user_register'),
    path('loggedinusers/', views.LoggedInUserList.as_view(), name='loggedinusers'),
    path('groups/', views.GroupsList.as_view(), name='groups'),
    path('modul-actives/', views.ModulosActivosList.as_view(), name='modul-actives'),
    path('accviewconf-list/', views.VistaConfigAccList.as_view(), name='accviewconf-list'),
]