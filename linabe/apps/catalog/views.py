from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from ..core.views import CommonViewSet
from .models import Category, Tag, CatalogMaster, CatalogDetail, CatalogDetailImage
from .serializers import (
    CategorySerializer,
    PublicCatalogSerializer,
    CategoryWithCompaniesSerializer,
    CategoryHierarchySerializer,
    TagSerializer,
    CatalogSerializer,
    CatalogCustomerSerializer,
    CatalogMasterSerializer,
    CatalogDetailSerializer,
    CatalogDetailImageSerializer,
)
from ..core.models import Customer, Cia

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import authentication, permissions, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .pdf import render_url_to_pdf, PdfOptions

import ulid


LinaUserModel = get_user_model()
# Create your views here.

# class CommonViewSet(ModelViewSet):
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
    http_method_names = ["get", "patch", "put", "post"]

    # queryset = CatalogMaster.objects.all()
    serializer_class = CatalogSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'created_at', 'is_active', 'created_by__username', 'customer__ulid', 'customer__name']
    ordering_fields = ['id', 'created_at', 'is_active', 'created_by__username', 'customer__ulid', 'customer__name']

    ordering = ['-created_at']

    def get_queryset(self):
        return CatalogMaster.objects.filter(owner=self.request.user)

    @action(detail=True, methods=["post"], url_path="export-pdf")
    def export_pdf(self, request, pk=None):
        catalog = self.get_object()

        # Asegura share_token para poder usar URL pública
        if not catalog.share_token:
            catalog.ensure_share_token()
            catalog.save(update_fields=["share_token"])

        base = settings.FRONTEND_BASE_URL.rstrip("/")
        url = f"{base}/portal/shared-catalog/{catalog.share_token}?pdf=1"

        landscape = catalog.orientation == "landscape"
        pdf_bytes = render_url_to_pdf(url, PdfOptions(landscape=landscape))

        filename = f"catalogo-{catalog.id}.pdf"
        resp = Response(
            pdf_bytes,
            status=status.HTTP_200_OK,
            content_type="application/pdf",
        )
        resp["Content-Disposition"] = f'attachment; filename="{filename}"'
        return resp

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
            return Response({'detail': 'Identificador inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Buscar el cliente
        try:
            customer = Customer.objects.get(ulid=ulid)
        except Customer.DoesNotExist:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtener catálogos vigentes (ttl >= fecha actual)
        now = timezone.now()
        catalogs = CatalogMaster.objects.filter(customer=customer, ttl__gte=now)

        catalog_serializer = CatalogMasterSerializer(catalogs, many=True)
        
        # Construir la respuesta con información del customer y los catálogos
        response_data = {
            'customer': {
                'id': customer.id,
                'name': customer.nombre,
                'email': customer.email,
                'ulid': customer.ulid,
            },
            'catalogs': catalog_serializer.data,
            'total_catalogs': catalogs.count()
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class ValidCustomerCatalogAPIView(APIView):
    """
    Devuelve un catálogo vigente de un cliente identificado por ULID y token.
    """

    authentication_classes = []
    permission_classes = []

    queryset = CatalogMaster.objects.all()
    serializer_class = CatalogCustomerSerializer

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
            catalog = CatalogMaster.objects.filter(
                customer=customer,
                token=token,
                ttl__gte=now
            ).prefetch_related('catalog_details', 'customer').first()
            
            if not catalog:
                return Response({'detail': 'Catálogo no encontrado o no vigente.'}, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response({'detail': 'Error al buscar el catálogo.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = CatalogCustomerSerializer(catalog)
        
        # Opción alternativa: Modificar respuesta manualmente
        # serializer = CatalogSerializer(catalog)
        # response_data = serializer.data.copy()
        # 
        # # Mapear campos con nombres alternativos
        # response_data['catalog_id'] = response_data.pop('id', None)
        # response_data['catalog_name'] = response_data.pop('name', None)
        # response_data['valid_until'] = response_data.pop('ttl', None)
        # response_data['access_token'] = response_data.pop('token', None)
        # 
        # return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesListAPIView(APIView):
    """
    1. Listado general de todas las categorías que incluya para qué compañías está disponible cada una.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """Retorna todas las categorías con información de compañías disponibles"""
        categories = Category.objects.filter(is_active=True).prefetch_related('available_for_companies')
        serializer = CategoryWithCompaniesSerializer(categories, many=True)
        
        return Response({
            'categories': serializer.data,
            'total': categories.count()
        }, status=status.HTTP_200_OK)


class TopCategoriesByCompanyAPIView(APIView):
    """
    2. Listado de categorías que no tengan padre y que estén disponibles para una Cia específica.
    Es decir los top fathers de una cía específica.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, company_id):
        """Retorna categorías padre (sin parent) disponibles para una compañía específica"""
        try:
            company = Cia.objects.get(id=company_id)
        except Cia.DoesNotExist:
            return Response({'detail': 'Compañía no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        # Categorías padre (sin parent) que están disponibles para esta compañía
        # O que no tienen restricciones de compañía (disponibles para todas)
        from django.db.models import Q
        
        top_categories = Category.objects.filter(
            parent__isnull=True,  # Sin padre (categorías raíz)
            is_active=True
        ).filter(
            Q(available_for_companies=company) |  # Disponible para esta compañía
            Q(available_for_companies__isnull=True)  # Sin restricciones
        ).distinct().prefetch_related('available_for_companies', 'children')

        serializer = CategoryHierarchySerializer(
            top_categories, 
            many=True, 
            context={'company_id': company_id, 'include_children': False}
        )
        
        return Response({
            'company': {
                'id': company.id,
                'codigo': company.codigo,
                'nombre': company.nombre
            },
            'top_categories': serializer.data,
            'total': top_categories.count()
        }, status=status.HTTP_200_OK)


class CategoriesByParentAndCompanyAPIView(APIView):
    """
    3. Listado de categorías dados un padre y Cía específicos.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, company_id, parent_id):
        """Retorna subcategorías de un padre específico disponibles para una compañía"""
        try:
            company = Cia.objects.get(id=company_id)
        except Cia.DoesNotExist:
            return Response({'detail': 'Compañía no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            parent_category = Category.objects.get(id=parent_id, is_active=True)
        except Category.DoesNotExist:
            return Response({'detail': 'Categoría padre no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        # Verificar que la categoría padre esté disponible para esta compañía
        if not parent_category.is_available_for_company(company):
            return Response({'detail': 'La categoría padre no está disponible para esta compañía.'}, 
                          status=status.HTTP_403_FORBIDDEN)

        # Obtener subcategorías del padre que estén disponibles para esta compañía
        from django.db.models import Q
        
        subcategories = Category.objects.filter(
            parent=parent_category,
            is_active=True
        ).filter(
            Q(available_for_companies=company) |  # Disponible para esta compañía
            Q(available_for_companies__isnull=True)  # Sin restricciones
        ).distinct().prefetch_related('available_for_companies', 'children')

        serializer = CategoryHierarchySerializer(
            subcategories, 
            many=True, 
            context={'company_id': company_id, 'include_children': True}
        )
        
        return Response({
            'company': {
                'id': company.id,
                'codigo': company.codigo,
                'nombre': company.nombre
            },
            'parent_category': {
                'id': parent_category.id,
                'name': parent_category.name,
                'description': parent_category.description
            },
            'subcategories': serializer.data,
            'total': subcategories.count()
        }, status=status.HTTP_200_OK)

class CatalogDetailView(generics.RetrieveAPIView):
    serializer_class = CatalogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Si tu app maneja company activa, filtra también por company_id aquí
        return CatalogMaster.objects.filter(owner=self.request.user)


class PublicCatalogByTokenView(generics.GenericAPIView):
    serializer_class = PublicCatalogSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        try:
            catalog = CatalogMaster.objects.get(share_token=token)
        except CatalogMaster.DoesNotExist:
            raise NotFound("Catalog not found")

        data = self.get_serializer(catalog).data
        return Response(data)
