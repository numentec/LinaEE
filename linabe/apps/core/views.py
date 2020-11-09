from django.shortcuts import render
from .models import Cia, User
from .serializers import CiaSerializer, UserSerializer, UserPermsSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Imports for Token Authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class LinaAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        fullname = '{} {}'.format(user.first_name, user.last_name)

        min_permissions = [
            'core.view_linabi_module',
            'core.view_user',
            'core.view_accounting_module',
            'core.view_hr_module',
            'core.view_cia',
            'core.add_cia',
            'core.view_purchase_module',
            'core.view_sys_module',
            'core.view_crm_module',
            'core.view_inv_module',
            'core.view_logistics_module',
            'core.view_sales_module'
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


class CiaList(ListAPIView):

    serializer_class = CiaSerializer

    def get_queryset(self):
        return Cia.objects.all()


class CiaDetail(RetrieveAPIView):

    serializer_class = CiaSerializer

    def get_queryset(self):
        return Cia.objects.all()


class UserList(ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class UserDetail(RetrieveAPIView):

    serializer_class = UserSerializer

    def get_object(self):

        pk = self.kwargs.get('pk')

        if pk == "cur":
            return self.request.user

        return super(UserDetail, self).get_object()

    def get_queryset(self):
        return User.objects.all()


class UserPermsDetail(RetrieveAPIView):

    serializer_class = UserPermsSerializer

    def get_object(self):

        pk = self.kwargs.get('pk')

        if pk == "cur":
            return self.request.user

        return super(UserPermsDetail, self).get_object()

    def get_queryset(self):
        return User.objects.all()