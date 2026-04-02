import os

from django.conf import settings
from django.utils import timezone
from django.utils.text import get_valid_filename
from django.http import HttpResponse, FileResponse, Http404
from django.contrib.auth import get_user_model
from rest_framework import parsers

from copy import deepcopy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import authentication, permissions, generics, status
from django.db import connections
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.viewsets import ModelViewSet

from urllib.parse import urljoin, urlencode
from urllib.parse import quote
import random

import ulid
import uuid

from ..core.models import SQLQuery
from ..core.views import CommonViewSet
from .models import (
    Category,
    Tag,
    CatalogMaster,
    CatalogDetail,
    CatalogDetailImage,
    PdfJob,
    genToken,
)
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
    MockProductSerializer,
    CatalogProductSerializer,
)
from ..core.models import Customer, Cia

from .pdf import render_url_to_pdf, PdfOptions
from .tasks import generate_catalog_pdf


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


CATALOG_IMAGE_LIBRARY = {
    'logos': os.path.join('images', 'catalogs', 'logos'),
    'covers': os.path.join('images', 'catalogs', 'covers'),
}

CATALOG_IMAGE_ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.svg'}
CATALOG_IMAGE_MAX_SIZE_BYTES = 5 * 1024 * 1024


def get_catalog_image_directory(asset_type):
    relative_dir = CATALOG_IMAGE_LIBRARY.get(asset_type)

    print(f"Asset type: {asset_type}, Relative dir: {relative_dir}")  # Debug log

    if not relative_dir:
        raise NotFound('Tipo de imagen no soportado.')

    absolute_dir = os.path.join(settings.MEDIA_ROOT, relative_dir)
    os.makedirs(absolute_dir, exist_ok=True)

    return relative_dir, absolute_dir


def build_catalog_image_payload(request, relative_dir, filename, absolute_path):
    relative_path = os.path.join(relative_dir, filename).replace('\\', '/')
    media_path = urljoin(settings.MEDIA_URL, relative_path)

    return {
        'name': filename,
        'url': request.build_absolute_uri(media_path),
        'relative_url': media_path,
        'size': os.path.getsize(absolute_path),
        'modified_at': timezone.datetime.fromtimestamp(
            os.path.getmtime(absolute_path),
            tz=timezone.utc,
        ).isoformat(),
    }


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

        job = PdfJob.objects.create(
            owner=request.user,
            catalog=catalog,
            status="queued",
        )

        generate_catalog_pdf.delay(str(job.id))

        return Response(
            {"job_id": str(job.id), "status": job.status},
            status=status.HTTP_202_ACCEPTED,
        )
        # base = settings.FRONTEND_BASE_URL.rstrip("/") + "/"

        # path = f"portal/shared-catalog/{catalog.share_token}/print"
        # query = urlencode({"pdf": "1"})
        # url = f"{base}/portal/shared-catalog/{catalog.share_token}/print?pdf=1"
        # url = urljoin(base, path) + "?" + query
        # # Ej: http://linafe:3001/portal/shared-catalog/<token>/print?pdf=1

        # landscape = catalog.orientation == "landscape"

        # try:
        #     pdf_bytes = render_url_to_pdf(url, PdfOptions(landscape=landscape))
        # except Exception as e:
        #     return HttpResponse(
        #         f"Error generating PDF: {str(e)}",
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         content_type="text/plain",
        #     )

        # filename = f"catalogo-{catalog.id}.pdf"

        # resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        # resp["Content-Disposition"] = f'attachment; filename="{filename}"'
        # return resp

    @action(detail=True, methods=['post'], url_path='duplicate')
    def duplicate(self, request, pk=None):
        source = self.get_object()

        duplicated = CatalogMaster.objects.create(
            company_id=source.company_id,
            name=f'{source.name} (copia)',
            template=source.template,
            orientation=source.orientation,
            status='draft',
            owner_id=request.user.id,
            settings=deepcopy(source.settings or {}),
            theme=deepcopy(source.theme or {}),
            pages=deepcopy(source.pages or []),
        )

        serializer = self.get_serializer(duplicated)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='ensure-share-token')
    def ensure_share_token(self, request, pk=None):
        catalog = self.get_object()

        if not catalog.share_token:
            catalog.ensure_share_token()
            catalog.save(update_fields=['share_token'])

        return Response(
            {'share_token': catalog.share_token},
            status=status.HTTP_200_OK,
        )


class CatalogImageLibraryAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get(self, request, asset_type):
        relative_dir, absolute_dir = get_catalog_image_directory(asset_type)

        items = []
        for entry in os.scandir(absolute_dir):
            if not entry.is_file():
                continue

            _, ext = os.path.splitext(entry.name)
            if ext.lower() not in CATALOG_IMAGE_ALLOWED_EXTENSIONS:
                continue

            items.append(
                build_catalog_image_payload(
                    request,
                    relative_dir,
                    entry.name,
                    entry.path,
                )
            )

        items.sort(key=lambda item: item['modified_at'], reverse=True)
        return Response({'results': items}, status=status.HTTP_200_OK)

    def post(self, request, asset_type):
        relative_dir, absolute_dir = get_catalog_image_directory(asset_type)
        upload = request.FILES.get('file')

        if not upload:
            return Response(
                {'detail': 'Debe adjuntar un archivo en el campo "file".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        _, ext = os.path.splitext(upload.name or '')
        ext = ext.lower()

        if ext not in CATALOG_IMAGE_ALLOWED_EXTENSIONS:
            return Response(
                {
                    'detail': (
                        'Formato no permitido. Use PNG, JPG, JPEG, WEBP o SVG.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if upload.size > CATALOG_IMAGE_MAX_SIZE_BYTES:
            return Response(
                {'detail': 'La imagen no puede exceder 5 MB.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        base_name = get_valid_filename(os.path.splitext(upload.name)[0]) or 'imagen'
        filename = f'{base_name}-{uuid.uuid4().hex[:8]}{ext}'
        absolute_path = os.path.join(absolute_dir, filename)

        with open(absolute_path, 'wb+') as destination:
            for chunk in upload.chunks():
                destination.write(chunk)

        payload = build_catalog_image_payload(
            request,
            relative_dir,
            filename,
            absolute_path,
        )

        return Response(payload, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='regenerate-share-token')
    def regenerate_share_token(self, request, pk=None):
        catalog = self.get_object()

        catalog.share_token = genToken()
        catalog.save(update_fields=['share_token'])

        return Response(
            {'share_token': catalog.share_token},
            status=status.HTTP_200_OK,
        )


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


class MockProductsAPIView(APIView):
    """
    Devuelve mock data de productos con el mismo contrato del frontend.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        count_raw = request.query_params.get("count", "200")
        try:
            count = int(count_raw)
        except (TypeError, ValueError):
            return Response(
                {"detail": "Parámetro 'count' inválido. Debe ser un número entero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if count < 1 or count > 1000:
            return Response(
                {"detail": "Parámetro 'count' fuera de rango. Use un valor entre 1 y 1000."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        brands = ["Nike", "Adidas", "Puma", "Lina"]
        products = []

        for i in range(count):
            n = i + 1
            sku = f"SKU-{n:04d}"

            image_count = random.randint(2, 4)
            images = []

            for j in range(image_count):
                seed_value = sku if j == 0 else f"{sku}+{j}"
                encoded_seed = quote(seed_value, safe="")
                images.append(
                    {
                        "url": f"https://picsum.photos/seed/{encoded_seed}/300",
                        "is_primary": j == 0,
                    }
                )

            products.append(
                {
                    "product_id": f"prod_{n}",
                    "sku": sku,
                    "description": f"Producto {n} descripción corta",
                    "brand_name": brands[i % 4],
                    "price": float(f"{5 + (i % 40) * 0.75:.2f}"),
                    "min_qty": (i % 6) + 1,
                    "max_qty": ((i % 6) + 1) * 12,
                    "images": images,
                    "selected_image_url": images[0]["url"],
                }
            )

        serializer = MockProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsAPIView(APIView):
    """
    Devuelve productos reales desde Oracle con paginación, filtros e imágenes locales.
    """
    authentication_classes = []
    permission_classes = []

    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
    MAIN_IMAGE_EXTENSIONS_ORDER = ['.jpg', '.jpeg', '.png']
    DEFAULT_PRODUCT_IMAGE_RELATIVE_PATH = os.path.join('images', 'no_image.png')
    ORACLE_PROC_NAME = os.environ.get(
        'ORACLE_PRODUCTS_CATALOG_PROC',
        'DMC.LINAEE_PROD_STYLE_CATALOG_SP',
    )

    def _build_default_image_url(self, request):
        relative_path = self.DEFAULT_PRODUCT_IMAGE_RELATIVE_PATH.replace('\\', '/')
        media_url = urljoin(settings.MEDIA_URL, relative_path)
        return request.build_absolute_uri(media_url)

    def _normalize_filter_value(self, raw_value):
        value = (raw_value or '').strip()
        return value or None

    def _parse_limit_offset(self, request):
        limit_raw = request.query_params.get('limit', '24')
        offset_raw = request.query_params.get('offset', '0')

        try:
            limit = int(limit_raw)
            offset = int(offset_raw)
        except (TypeError, ValueError):
            raise ValueError("Parámetros 'limit' y 'offset' deben ser enteros.")

        if limit < 1 or limit > 200:
            raise ValueError("Parámetro 'limit' fuera de rango. Use un valor entre 1 y 200.")
        if offset < 0:
            raise ValueError("Parámetro 'offset' inválido. Debe ser mayor o igual a 0.")

        return limit, offset

    def _to_float(self, value, default=0.0):
        if value is None:
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _to_int(self, value, default=0):
        if value is None:
            return default
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _build_page_link(self, request, offset, limit):
        query_params = request.query_params.copy()
        query_params['offset'] = str(offset)
        query_params['limit'] = str(limit)
        return f"{request.build_absolute_uri(request.path)}?{query_params.urlencode()}"

    def _resolve_product_images(self, request, sku):
        sku_value = (sku or '').strip()
        if not sku_value:
            return []

        fotos_root = os.path.join(settings.MEDIA_ROOT, 'fotos')
        if not os.path.isdir(fotos_root):
            return []

        images = []
        primary_url = None

        for ext in self.MAIN_IMAGE_EXTENSIONS_ORDER:
            candidate_name = f'{sku_value}{ext}'
            candidate_path = os.path.join(fotos_root, candidate_name)
            if os.path.isfile(candidate_path):
                relative_path = os.path.join('fotos', candidate_name).replace('\\\\', '/')
                media_url = urljoin(settings.MEDIA_URL, relative_path)
                primary_url = request.build_absolute_uri(media_url)
                images.append({'url': primary_url, 'is_primary': True})
                break

        gallery_path = os.path.join(fotos_root, sku_value)
        if os.path.isdir(gallery_path):
            for entry in sorted(os.scandir(gallery_path), key=lambda item: item.name.lower()):
                if not entry.is_file():
                    continue

                _, ext = os.path.splitext(entry.name)
                if ext.lower() not in self.IMAGE_EXTENSIONS:
                    continue

                relative_path = os.path.join('fotos', sku_value, entry.name).replace('\\\\', '/')
                media_url = urljoin(settings.MEDIA_URL, relative_path)
                image_url = request.build_absolute_uri(media_url)

                if image_url == primary_url:
                    continue

                images.append({'url': image_url, 'is_primary': False})

        if not images:
            images.append(
                {
                    'url': self._build_default_image_url(request),
                    'is_primary': True,
                }
            )

        return images

    def _fetch_products_from_oracle(self, filters, limit, offset):
        with connections['extdb1'].cursor() as cursor:
            ref_cursor = cursor.connection.cursor()
            params = [
                filters.get('cia'),
                filters.get('search'),
                filters.get('brand'),
                filters.get('departamento'),
                filters.get('categoria'),
                filters.get('subcategoria'),
                offset,
                limit,
                ref_cursor,
            ]

            cursor.callproc(self.ORACLE_PROC_NAME, params)
            columns = [column[0] for column in (ref_cursor.description or [])]
            rows = ref_cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    def get(self, request):
        try:
            limit, offset = self._parse_limit_offset(request)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        filters = {
            'cia': self._normalize_filter_value(request.query_params.get('cia')),
            'search': self._normalize_filter_value(request.query_params.get('search')),
            'brand': self._normalize_filter_value(request.query_params.get('brand')),
            'departamento': self._normalize_filter_value(request.query_params.get('departamento')),
            'categoria': self._normalize_filter_value(request.query_params.get('categoria')),
            'subcategoria': self._normalize_filter_value(request.query_params.get('subcategoria')),
        }

        try:
            rows = self._fetch_products_from_oracle(filters, limit, offset)
        except Exception as exc:
            return Response(
                {'detail': 'No fue posible consultar productos en la base de datos.', 'error': str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        products = []
        total_count = 0

        for row in rows:
            images = self._resolve_product_images(request, row.get('SKU'))
            selected_image_url = None
            if images:
                selected_image_url = next(
                    (image['url'] for image in images if image.get('is_primary')),
                    images[0]['url'],
                )

            row_total = row.get('TOTAL_COUNT')
            if row_total is not None:
                total_count = self._to_int(row_total, default=total_count)

            products.append(
                {
                    'product_id': str(row.get('ID', '') or ''),
                    'sku': str(row.get('SKU', '') or ''),
                    'description': str(row.get('DESCRIP', '') or ''),
                    'brand_name': str(row.get('MARCA', '') or ''),
                    'price': self._to_float(row.get('PRECIO'), default=0.0),
                    'min_qty': self._to_int(row.get('MIN_QTY'), default=1),
                    'max_qty': self._to_int(row.get('MAX_QTY'), default=1),
                    'departamento': str(row.get('DEPARTAMENTO', '') or ''),
                    'categoria': str(row.get('CATEGORIA', '') or ''),
                    'subcategoria': str(row.get('SUBCATEGORIA', '') or ''),
                    'images': images,
                    'selected_image_url': selected_image_url,
                }
            )

        if not rows:
            total_count = 0
        elif total_count <= 0:
            total_count = offset + len(products)

        next_offset = offset + limit
        has_next = next_offset < total_count
        previous_offset = max(offset - limit, 0) if offset > 0 else None

        serializer = CatalogProductSerializer(products, many=True)
        return Response(
            {
                'count': total_count,
                'limit': limit,
                'offset': offset,
                'next': self._build_page_link(request, next_offset, limit) if has_next else None,
                'previous': self._build_page_link(request, previous_offset, limit) if previous_offset is not None else None,
                'results': serializer.data,
            },
            status=status.HTTP_200_OK,
        )

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


class CommonListsAPIView(APIView):
    """Listas de parámetros comunes (clientes, vendedores, categorías, etc."""
    # Vista 39
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, company_id='01', list_type='X'):
        # list_type - Tipo de lista (CLI, PROV, VEN, MAR, DEP, CLA, SCLA)

        if list_type == 'X':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        result = []

        # query = SQLQuery.objects.get(vista = 39, ordinal = 1)

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc('DMC.LINAEE_LISTCATS', [list_type, company_id, refCursor])
            # cursor.callproc(query.content, [list_type, company_id, refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)