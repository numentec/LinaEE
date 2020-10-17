from django.shortcuts import render
from .models import Cia, User
from .serializers import CiaSerializer, UserSerializer
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

    def get_queryset(self):
        return User.objects.all()