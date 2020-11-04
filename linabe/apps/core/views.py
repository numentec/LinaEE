from django.shortcuts import render
from .models import Cia, User
from .serializers import CiaSerializer, UserSerializer, UserPermsSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
# Create your views here.


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