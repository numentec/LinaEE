from django.utils import timezone
from django.contrib.auth import get_user_model
from ..core.views import CommonViewSet
from .models import Category, Tag, CatalogMaster, CatalogDetail, CatalogDetailImage
from .serializers import (
    CategorySerializer,
    TagSerializer,
    CatalogSerializer,
    CatalogMasterSerializer,
    CatalogDetailSerializer,
    CatalogDetailImageSerializer,
)
from ..core.models import Customer

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

import ulid


LinaUserModel = get_user_model()
# Create your views here.

# class CommonViewSet(viewsets.ModelViewSet):
#     """Ensure the models are updated with the requesting user."""

#     def perform_create(self, serializer):
#         """Ensure we have the authorized user for ownership."""
#         serializer.save(created_by=self.request.user, modified_by=self.request.user)

#     def perform_update(self, serializer):
#         """Ensure we have the authorized user for ownership."""
#         serializer.save(modified_by=self.request.user)


def is_ulid(valor):
    try:
        ulid.ULID.from_str(valor)
        return True
    except (ValueError, TypeError):
        return False


class CategoryViewSet(CommonViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(CommonViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CatalogMasterViewSet(CommonViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = CatalogMaster.objects.all()
    serializer_class = CatalogMasterSerializer

class CatalogDetailViewSet(CommonViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = CatalogDetail.objects.all()
    serializer_class = CatalogDetailSerializer

class CatalogDetailImageViewSet(CommonViewSet):
    queryset = CatalogDetailImage.objects.all()
    serializer_class = CatalogDetailImageSerializer


class CatalogViewSet(CommonViewSet):
    """
    A simple ViewSet for viewing and editing Catalog.
    Including the details (items) associated with each catalog.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = CatalogMaster.objects.all()
    serializer_class = CatalogSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'created_at', 'is_active', 'created_by__username', 'customer__ulid', 'customer__name']
    ordering_fields = ['id', 'created_at', 'is_active', 'created_by__username', 'customer__ulid', 'customer__name']

    ordering = ['-created_at']


class ActiveCustomerCatalogsAPIView(APIView):
    """
    Devuelve los catálogos vigentes de un cliente identificado por ULID.
    """

    authentication_classes = []
    permission_classes = []

    queryset = CatalogMaster.objects.all()
    serializer_class = CatalogMasterSerializer

    def get(self, request, ulid):
        # Validar que el parámetro sea un ULID válido
        if not is_ulid(ulid):
            return Response({'detail': 'ULID inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Buscar el cliente
        try:
            customer = Customer.objects.get(ulid=ulid)
        except Customer.DoesNotExist:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtener catálogos vigentes (ttl >= fecha actual)
        now = timezone.now()
        catalogs = CatalogMaster.objects.filter(customer=customer, ttl__gte=now)

        serializer = CatalogMasterSerializer(catalogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ValidCustomerCatalogAPIView(APIView):
    """
    Devuelve un catálogo vigente de un cliente identificado por ULID y token.
    """
    queryset = CatalogMaster.objects.all()
    serializer_class = CatalogSerializer

    def get(self, request, ulid, token):
        # Validar que el parámetro sea un ULID válido
        if not is_ulid(ulid):
            return Response({'detail': 'Identificador inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Buscar el cliente
        try:
            customer = Customer.objects.get(ulid=ulid)
        except Customer.DoesNotExist:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtener el catálogo vigente con el token dado
        now = timezone.now()
        try:
            catalog = CatalogMaster.objects.get(
                customer=customer,
                token=token,
                ttl__gte=now
            )
        except CatalogMaster.DoesNotExist:
            return Response({'detail': 'Catálogo no encontrado o no vigente.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CatalogSerializer(catalog)
        return Response(serializer.data, status=status.HTTP_200_OK)
