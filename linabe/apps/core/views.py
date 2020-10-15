from django.shortcuts import render
from .models import Cia
from .serializers import CiaSerializer
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