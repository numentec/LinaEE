import django.core.serializers as ss
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Cia, StakeHolder, User
from .serializers import (
    CiaSerializer,
    UserSerializer,
    UserFotoSerializer,
    UserPermsSerializer,
    UserRegisterSerializer,
    ProfileSerializer,
    GroupsSerializer,
    StakeHolderSerializer,
    RenewPasswordSerializer,
)
from apps.core import models
from apps.core import serializers
# from linapi.permissions import CustomDjangoModelPermissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework import viewsets, status
from rest_framework.decorators import action

# Imports for Token Authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings

import json

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

        # groups = serializers.SlugRelatedField(
        #     many=True,
        #     read_only=True,
        #     slug_field='name',
        # )

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

        if user.foto and hasattr(user.foto, 'url') :
            ufoto = user.foto.url
        else:
            ufoto = ''

        # Grupos del usuario (por nombre de grupo)
        if user.groups :
            ugroups = user.groups.values_list('name', flat=True)
        else:
            ugroups = []

        return Response({
            'token': token.key,
            'user': {
                'id': user.pk,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'fullname': fullname,
                'foto': ufoto,
                'perms': perms,
                'is_superuser': user.is_superuser,
                'ugroups': ugroups
            }
        })


class CommonViewSet(viewsets.ModelViewSet):
    """Ensure the models are updated with the requesting user."""

    def perform_create(self, serializer):
        """Ensure we have the authorized user for ownership."""
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        """Ensure we have the authorized user for ownership."""
        serializer.save(modified_by=self.request.user)


class CiaViewSet(CommonViewSet):
    """ViewSet de compañías"""
    serializer_class = CiaSerializer
    # permission_classes = (CustomDjangoModelPermissions, )

    queryset = Cia.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        action = self.action
        
        if (action == 'list'):
            context['fields'] = ('id', 'codigo', 'nombre_corto', 'ruc', 'tel1', 'email', 'is_active')
        # elif (action == 'create'):
        #     context['fields'] = ('id',)
        # elif (action == 'retrieve'):
        #     context['fields'] = ('title', 'author', 'isbn', 'price', 'synopsis')
        return context

    def get_queryset(self):
        return Cia.objects.all()


class StakeHolderViewSet(CommonViewSet):
    """ViewSet de stakeholders"""
    serializer_class = StakeHolderSerializer
    # permission_classes = (CustomDjangoModelPermissions, )

    queryset = StakeHolder.stakeholders.all()

    # def get_queryset(self):
    #     shtype = self.request.query_params.get('shtype')
    #     queryset = StakeHolder.objects.get_StakeHolders(shtype)()
    #     return queryset

    def get_serializer_context(self):
        shtype = self.request.query_params.get('shtype')
        context = super().get_serializer_context()
        action = self.action
        
        if (action == 'list' and 'short' in shtype):
            context['fields'] = ('id', 'codigo', 'nombre', 'ruc', 'tel1', 'email')
        return context

    def list(self, request):
        shtype = request.query_params.get('shtype')
        only_actives = request.query_params.get('only_actives')

        if only_actives:
            queryset = StakeHolder.stakeholders.get_StakeHolders(shtype, only_actives)
        else:
            queryset = StakeHolder.stakeholders.get_StakeHolders(shtype)

        serializer = self.get_serializer(queryset, many=True)
        resultset = serializer.data

        return Response(resultset)


class UserList(ListAPIView):
    """Lista de usuarios"""
    serializer_class = UserSerializer
    # permission_classes = (CustomDjangoModelPermissions, )

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
    serializer_class = UserRegisterSerializer

    def get_queryset(self):
        return LinaUserModel.objects.filter(is_active=True)


class ProfileViewSet(viewsets.ModelViewSet):
    """Administrar perfil de usuarios"""
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return LinaUserModel.objects.filter(is_active=True).order_by('-id')
    
    def get_serializer_class(self):
        """Retornar serializer requerido"""
        if self.action == 'retrieve':
            return UserSerializer
        elif self.action == 'create':
            return UserRegisterSerializer
        elif self.action == 'upload_foto':
            return UserFotoSerializer
        elif self.action == 'renew_pass':
            return RenewPasswordSerializer

        return self.serializer_class

    @action(methods=['POST',], detail=True, url_path='upload-foto')
    def upload_foto(self, request, pk=None):
        """Subir foto de perfil"""
        perfil = self.get_object()
        serializer = self.get_serializer(perfil, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT',], detail=True, url_path='renew-pass')
    def renew_pass(self, request, pk=None):
        """Renovar contraseña"""
        perfil = self.get_object()
        serializer = self.get_serializer(perfil, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RenewPasswordView(UpdateAPIView):

    serializer_class = RenewPasswordSerializer
    
    def get_queryset(self):
        return LinaUserModel.objects.filter(is_active=True).order_by('-id')


class GroupsList(ListAPIView):
    """Lista de grupos de usuarios"""
    serializer_class = GroupsSerializer

    def get_queryset(self):
        return Group.objects.all()


class ModuloViewSet(CommonViewSet):
    """ViewSet de módulos"""
    serializer_class = serializers.ModuloSerializer
    # permission_classes = (CustomDjangoModelPermissions, )

    def get_queryset(self):
        return models.Modulo.objects.all()

class ModulosActivosList(ListAPIView):
    """Lista de módulos disponibles"""
    serializer_class = serializers.ModuloSerializer

    def get_queryset(self):
        return models.Modulo.objects.filter(is_active=True)

class VistaViewSet(CommonViewSet):
    """ViewSet de vistas"""
    serializer_class = serializers.VistaSerializer
    # permission_classes = (CustomDjangoModelPermissions, )

    def get_queryset(self):
        return models.Vista.objects.all()


class VistaConfigViewSet(CommonViewSet):
    """ViewSet de configuraciones por vista"""
    serializer_class = serializers.VistaConfigSerializer
    # permission_classes = (CustomDjangoModelPermissions, )

    def get_queryset(self):
        return models.VistaConfig.objects.all()


class VistaConfigUserViewSet(CommonViewSet):
    """ViewSet de configuraciones por vista por usuario"""
    serializer_class = serializers.VistaConfigUserSerializer
    # permission_classes = (CustomDjangoModelPermissions, )

    def get_queryset(self):
        return models.VistaConfigUser.objects.all()


class VistaConfigAccViewSet(viewsets.ModelViewSet):
    """ViewSet de accesos a configuraciones por vista"""
    serializer_class = serializers.VistaConfigAccSerializer
    # permission_classes = (CustomDjangoModelPermissions, )

    def get_queryset(self):
        return models.VistaConfigAcc.objects.all()


class VistaConfigAccList(ListAPIView):
    """ListAPI para filtrar los permisos de un grupo para una vista específica"""
    model = models.VistaConfigAcc
    serializer_class = serializers.VistaConfigAccSerializer
    # permission_classes = (CustomDjangoModelPermissions, )

    def get_queryset(self):
        idv = self.request.query_params.get('idvista', 0)
        groups = self.request.query_params.get('groups', '')
        glist = list(groups.split(','))

        if int(idv) > 0 and len(glist) > 0:
            acclist = models.VistaConfigAcc.objects \
                .filter(vistaconf__vista__id=idv, group__name__in=glist, acceso=True)
            # #         .values('vistaconf_id').distinct()
        else:
            acclist = models.VistaConfigAcc.objects.all()

        return acclist


# class VistaElementViewSet(CommonViewSet):
#     """ViewSet de elementos de vista"""
#     serializer_class = serializers.VistaElementSerializer
#     permission_classes = (CustomDjangoModelPermissions, )

#     def get_queryset(self):
#         return models.VistaElement.objects.all()


# class VistaElementAccessViewSet(CommonViewSet):
#     """ViewSet de elementos de vista"""
#     serializer_class = serializers.VistaElementAccessSerializer
#     permission_classes = (CustomDjangoModelPermissions, )

#     def get_queryset(self):
#         return models.VistaElementAccess.objects.all()


# class VistaElAccList(ListAPIView):
#     """ListAPI para filtrar los permisos de un grupo para una vista específica"""
#     serializer_class = serializers.VistaElementAccessSerializer
#     permission_classes = (IsAuthenticated, )

#     def get_queryset(self):
#         idvista = self.kwargs['idvista']
#         idgroup = self.kwargs['idgroup']

#         acclist = models.VistaElementAccess.objects \
#             .filter(vista_element__vista__id=idvista, group__id=idgroup)

#         return acclist
