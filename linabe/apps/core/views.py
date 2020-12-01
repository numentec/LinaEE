from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Cia, User
from .serializers import (
    CiaSerializer,
    UserSerializer,
    UserPermsSerializer,
    UserRegisterSerializer,
    GroupsSerializer
)

from linapi.permissions import CustomDjangoModelPermissions
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import viewsets

# Imports for Token Authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings

LinaUserModel = get_user_model()

class LinaAuthToken(ObtainAuthToken):
    """Autenticación por token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        fullname = '{} {}'.format(user.first_name, user.last_name)

        min_permissions = [
            'core.view_module_linabi',
            'core.view_user',
            'core.view_module_accounting',
            'core.view_module_hr',
            'core.view_cia',
            'core.add_cia',
            'core.view_module_purchase',
            'core.view_module_sys',
            'core.view_module_crm',
            'core.view_module_inv',
            'core.view_module_logistics',
            'core.view_module_sales'
            ]

        #all_permissions = User(is_superuser=True).get_all_permissions()
        user_permissions = user.get_all_permissions()

        perms = {p: p in user_permissions for p in min_permissions}

        return Response({
            'token': token.key,
            'user': {
                'id': user.pk,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'fullname': fullname,
                'perms': perms
            }
        })


class CiaViewSet(viewsets.ModelViewSet):
    """ViewSet de compañías"""
    serializer_class = CiaSerializer
    permission_classes = (CustomDjangoModelPermissions, )

    queryset = Cia.objects.all()


class UserList(ListAPIView):
    """Lista de usuarios"""
    serializer_class = UserSerializer
    permission_classes = (CustomDjangoModelPermissions, )

    queryset = User.objects.none()

    def get_queryset(self):
        username = self.kwargs['username']

        if(username == 'actives'):
            userslist = LinaUserModel.objects.filter(is_active=True).order_by('-id')
        elif(username == 'all'):
            userslist = LinaUserModel.objects.all().order_by('-id')
        else:
            userslist = LinaUserModel.objects.filter(username__icontains=username).order_by('-id')

        return userslist


class UserDetail(RetrieveAPIView):
    """Detalles del usuario"""
    serializer_class = UserSerializer

    def get_object(self):

        pk = self.kwargs.get('pk')

        if pk == "cur":
            return self.request.user

        return super(UserDetail, self).get_object()

    def get_queryset(self):
        return User.objects.all().order_by('-id')


class UserPermsDetail(RetrieveAPIView):
    """Datos y permisos del usuario"""
    serializer_class = UserPermsSerializer

    def get_object(self):

        pk = self.kwargs.get('pk')

        if pk == "cur":
            return self.request.user

        return super(UserPermsDetail, self).get_object()

    def get_queryset(self):
        return LinaUserModel.objects.all()


class UserRegister(CreateAPIView):
    """Registrar un nuevo usuario"""
    # serializer_class = UserSerializer
    serializer_class = UserRegisterSerializer

    def get_queryset(self):
        return LinaUserModel.objects.filter(is_active=True)


class GroupsList(ListAPIView):
    """Lista de grupos de usuarios"""
    serializer_class = GroupsSerializer

    def get_queryset(self):
        return Group.objects.all()