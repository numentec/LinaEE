from lib2to3.pgen2 import token
from urllib import request
from django.db.models import Prefetch
from django.conf import settings
from django.shortcuts import render
from django.db import connections
from django.contrib.auth import get_user_model
# from django.contrib.auth import user_login_failed, user_logged_in
from django.contrib.auth.models import Group, update_last_login
from django.contrib.sessions.serializers import  JSONSerializer
from .models import Cia, StakeHolder, User, IpWhiteList
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
from rest_framework import authentication, permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import action

# Imports for Token Authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.exceptions import PermissionDenied, NotFound
from django.contrib.sessions.models import Session
from django.utils import timezone

from django.core import serializers as srlzrs
from django.contrib.sessions.backends.db import SessionStore
import json
import datetime
from socket import error as SocketError
import errno

from ipware import get_client_ip

LinaUserModel = get_user_model()

# def lina_update_last_login(sender, user, **kwargs):
#     # user.app_last_login = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
#     curtime = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
#     user.app_last_login = curtime
#     user.save(update_fields=['app_last_login'])

# Listar usuarios con sesión iniciada
def get_all_logged_in_users(opc = 1):
    # Query all non-expired sessions
    # sessions = Session.objects.filter(expire_date__gte=timezone.now())
    sessions = Session.objects.filter(expire_date__gte=timezone.localtime(timezone.now()))

    uid_list = []
    udata_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()

        uid = data.get('_auth_user_id', None)
        fip = data.get('from_IP', None)
        ltime = data.get('loggin_time', None)
        uname = data.get('auth_username', None)
        fname = data.get('fullname', None)

        el = {'id': uid, 'username': uname, 'fullname': fname, 'fromip': fip, 'last_login': ltime}

        uid_list.append(uid)
        udata_list.append(el)
        print('***** SESSION *****', session)

    if opc == 1:
        return LinaUserModel.objects.filter(id__in=uid_list).values('id', 'username', 'last_login')
    else:
        return udata_list


class LinaAuthToken(ObtainAuthToken):
    """Autenticación por token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # print(f'REQUEST META: {request.META}')
        pc = getattr(settings, 'PROXY_COUNT', 0)
        ptips = getattr(settings, 'PROXY_TRUSTED', [])

        #client_ip, is_routable = get_client_ip(request, request_header_order=['X_FORWARDED_FOR', 'REMOTE_ADDR'], proxy_count=pc, proxy_trusted_ips=ptips)
        client_ip, is_routable = get_client_ip(request, request_header_order=['REMOTE_ADDR', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_REAL_IP'])
        # print('***** REQUEST *****\n', request.META)
        # print('***** CLIENTIP *****\n', client_ip)
        # print('***** ISROUTABLE *****\n', is_routable)

        nowtime = timezone.localtime(timezone.now()).strftime("%H:%M:%S")

        if client_ip is None:
            # Unable to get the client's IP address
            raise PermissionDenied("No se pudo comprobar la dirección de origen")
        else:
            # We got the client's IP address
            try:
                ipwl = IpWhiteList.objects.get(
                    ip_address=client_ip,
                    hora_ini__lt=nowtime,
                    hora_fin__gt=nowtime
                )
                if ipwl.reject:
                    raise PermissionDenied("Acceso denegado para este origen")
            except IpWhiteList.DoesNotExist:
                
                if is_routable:
                    # The client's IP address is publicly routable on the Internet
                    if not user.has_perm('core.ext_acc'):
                        raise PermissionDenied("Solo puede acceder desde la Intranet")
                # else:
                #     # The client's IP address is private
                #     print(f'IP INTERNA: {client_ip}')


        token, created = Token.objects.get_or_create(user=user)

        fullname = '{} {}'.format(user.first_name, user.last_name)

        request.session['_auth_user_id'] = user.id
        request.session['auth_username'] = user.username
        request.session['fullname'] = fullname
        request.session['from_IP'] = client_ip
        request.session['loggin_time'] = timezone.localtime(timezone.now()).strftime("%d/%m/%Y %H:%M:%S")

        # groups = serializers.SlugRelatedField(
        #     many=True,
        #     read_only=True,
        #     slug_field='name',
        # )

        min_permissions = [
            'core.acc_crm',
            'core.acc_sales',
            'core.acc_purchase',
            'core.acc_inv',
            'core.acc_hr',
            'core.acc_accounting',
            'core.acc_logistics',
            'core.acc_linabi',
            'core.acc_config',
            'core.acc_wms',
            'core.acc_wms_relocate_tool',
            'core.acc_wms_qryoneprod_tool',
            'core.view_user',
            'core.view_cia',
            'core.add_cia',
            'core.acc_linabi_catalog',
            'core.acc_linabi_saledocs_master',
            'core.acc_linabi_saledocs_datail',
            'core.acc_linabi_sales_detail',
            'core.acc_linabi_reports',
            'core.acc_linabi_storagexloc',
            'core.acc_linabi_listcli',
            'core.acc_linabi_panel',
            'core.ext_acc'
            ]

        # all_permissions = User(is_superuser=True).get_all_permissions()
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

        update_last_login(None, user)

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
                'ugroups': ugroups,
                'homelink': user.homelink
            }
        })
# user_logged_in.disconnect(update_last_login, dispatch_uid='update_last_login')
# user_logged_in.connect(lina_update_last_login, dispatch_uid='lina_update_last_login')

class LogOut(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # force = int(request.query_params.get('force', '0'))
            force = 0
            if request.body:
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                force = int(body['force'])

            user = request.user
            token = Token.objects.filter(user=user).first()

            if token:
                sessions = Session.objects.filter(expire_date__gte=timezone.localtime(timezone.now()))
                if sessions.exists():
                    for session in sessions:
                        data = session.get_decoded()

                        if user.id == int(data.get('_auth_user_id')):
                            session.delete()

                if not user.is_superuser:
                    token.delete()

                if force == 1:
                    print('***** Fin de sesión forzado *****')

                return Response({'message': 'Sesion finalizada'}, status = status.HTTP_200_OK)

            return Response({'error': 'Credenciales inválidas'}, status = status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error': 'Error finalizando sesión'}, status = status.HTTP_409_CONFLICT)


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

    queryset = Cia.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        action = self.action
        
        if (action == 'list'):
            context['fields'] = ('id', 'codigo', 'nombre_corto', 'ruc', 'tel1', 'email', 'extrel', 'default', 'is_active')
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


class LoggedInUsers(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        result = get_all_logged_in_users(2)
        return Response(result, status=status.HTTP_200_OK)


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


class ModuloViewSet(viewsets.ModelViewSet):
    """ViewSet de módulos"""
    serializer_class = serializers.ModuloSerializer

    def get_queryset(self):
        return models.Modulo.objects.all()

class ModulosActivosList(ListAPIView):
    """Lista de módulos disponibles"""
    serializer_class = serializers.ModulosActLstSerializer

    def get_queryset(self):
        return models.Modulo.objects.filter(is_active=True)
# class ModulosActivosList(ListAPIView):
#     """Lista de módulos disponibles"""
#     serializer_class = serializers.ModuloSerializer

#     def get_queryset(self):
#         try:
#             resp = models.Modulo.objects.filter(is_active=True)
#         except SocketError as e:
#             if e.errno != errno.ECONNRESET:
#                 raise NotFound("Error en Socket")

#         return resp


class VistaViewSet(CommonViewSet):
    """ViewSet de vistas"""
    serializer_class = serializers.VistaSerializer
    # permission_classes = (CustomDjangoModelPermissions, )

    lookup_value_regex = '\d+'

    def get_queryset(self):
        colsExcluded = []

        pk = self.kwargs.get('pk')

        if pk:
            colsExcluded = self.request.user.colsToRemoveTmp(int(pk))

        queryset = models.Vista.objects.prefetch_related(Prefetch(
            'configs_x_vista', queryset=models.VistaConfig.objects.exclude(configkey__in = colsExcluded)))

        return queryset


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


class SQLQueryViewSet(CommonViewSet):
    """ViewSet de SQL queries"""
    serializer_class = serializers.SQLQuerySerializer

    def get_queryset(self):
        return models.SQLQuery.objects.all()


class UsrExtRelListAPIView(APIView):
    """Relación externa para los usuarios."""
    # Vista 27
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        result = []

        qry = models.SQLQuery.objects.get(vista = 27, ordinal = 1)

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            # cursor.callproc('DMC.LINAEE_USREXTREL', [refCursor])
            cursor.callproc(qry.content, [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)

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
