from django.db import connections
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import authentication, permissions
from rest_framework import status
from drf_dx_datagrid import DxModelViewSet
from .models import BICatalog, BIFavorito
from .serializers import BICatalogSerializer, BIFavoritoSerializer
from ..core.views import CommonViewSet


class ListAsQuerySet(list):
    """Convertir una lista a queryset"""
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self  # filter ignoring, but you can impl custom filter

    def order_by(self, *args, **kwargs):
        return self

class CommonListsAPIView(APIView):
    """Listas de parámetros comunes (clientes, vendedores, categorías, etc."""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - Tipo de lista (CLI, PROV, VEN, MAR, CLA1, CLA2, CLA3, CLAX)

        p01 = str(request.query_params.get('p01', 'X'))

        if p01 == 'X':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        result = []

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc('DMC.LINA_LISTS', [p01, refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)

class TallasBCAPIView(APIView):
    """Lista de codigo de barras por talla"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        sku = str(request.query_params.get('sku', 'X')).lower()

        if sku == 'X':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [sku]

        result = []

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc('DMC.LINA_TALLASBC', params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class CatalogModelViewSet(DxModelViewSet):
# class CatalogModelViewSet(viewsets.ModelViewSet):
    """Catálogo - Lista de productos"""
    serializer_class = BICatalogSerializer
    # queryset = BICatalog.objects.all()

    def get_queryset(self):
        p01 = str(self.request.query_params.get('p01', '%')).lower()
        p02 = str(self.request.query_params.get('p02', 'camisa%')).lower()
        p03 = str(self.request.query_params.get('p03', '%')).lower()
        p04 = str(self.request.query_params.get('p04', '%')).lower()
        p05 = str(self.request.query_params.get('p05', '%')).lower()
        p06 = str(self.request.query_params.get('p06', '%')).lower()
        p07 = str(self.request.query_params.get('p07', '%')).lower()
        p08 = str(self.request.query_params.get('p08', '%')).lower()
        p09 = str(self.request.query_params.get('p09', '%')).lower()
        p10 = str(self.request.query_params.get('p10', '%')).lower()
        p11 = str(self.request.query_params.get('p11', 0)).lower()
        p12 = str(self.request.query_params.get('p12', '2021-01-01')).lower()
        p13 = str(self.request.query_params.get('p13', '2021-01-01')).lower()
        p14 = str(self.request.query_params.get('p14', '1')).lower()

        print(p02)

        params = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14]

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc('DMC.LINA_QRYCATALOGO', params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        qs = ListAsQuerySet(result, model=BICatalog)

        return qs


class CatalogAPIView(APIView):
    """Catálogo - Lista de productos"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - SKU exacto o parcial con %
        # p02 - Descripción parcial con %
        # p03 - Marca 
        # p04 - Departamento
        # p05 - Categoría
        # p06 - Sub categoría
        # p07 - Cla1
        # p08 - Cla2
        # p09 - Cla3
        # p10 - Número de entrada
        # p11 - Tipo de consulta: incluir periodo (0, 1)
        # p12 - Fecha inicial del periodo a consultar
        # p13 - Fecha final del periodo a consultar
        # p14 - Existencia (Todos = 1, Disponible = 2, A futuro = 3)
        p01 = str(request.query_params.get('p01', '%')).lower()
        p02 = str(request.query_params.get('p02', '%')).lower()
        p03 = str(request.query_params.get('p03', '%')).lower()
        p04 = str(request.query_params.get('p04', '%')).lower()
        p05 = str(request.query_params.get('p05', '%')).lower()
        p06 = str(request.query_params.get('p06', '%')).lower()
        p07 = str(request.query_params.get('p07', '%')).lower()
        p08 = str(request.query_params.get('p08', '%')).lower()
        p09 = str(request.query_params.get('p09', '%')).lower()
        p10 = str(request.query_params.get('p10', '%')).lower()
        p11 = str(request.query_params.get('p11', 0)).lower()
        p12 = str(request.query_params.get('p12', '2021-01-01')).lower()
        p13 = str(request.query_params.get('p13', '2021-01-01')).lower()
        p14 = str(request.query_params.get('p14', '1')).lower()

        pvals = p01 + p02 + p03 + p04 + p05 + p06 + p07 + p08 + p09 + p10 + p11 + p12 + p13 + p14

        if pvals == '%%%%%%%%%%022021-01-012021-01-011':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14]

        result = []
        qrycalling = 'DMC.LINAEE_QRYCATALOGO'
        skulist = False

        # Preparar lista de SKUs o codigos de barra
        if (',' in p01):
            p01 = p01.replace(' ', '')
            skulist = True
        elif (' ' in p01):
            p01 = p01.replace(' ', ',')
            skulist = True

        if skulist:
            if (p02 not in ['sku', 'bc']):
                p02 = 'SKU'
            params = [p01, p02]
            qrycalling = 'DMC.LINAEE_QRYCATALOGO_SKU'

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class SaleDocsMAPIView(APIView):
    """Documentos de ventas"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - Lista con los números de documentos a consultar
        # p02 - Código del cliente
        # p03 - Código de vendedor
        # p11 - Tipo de consulta: Listado por números de documentos, por periodo (0, 1)
        # p12 - Fecha inicial del periodo a consultar
        # p13 - Fecha final del periodo a consultar
        # p15 - Tipo de documento: Cotización (COT), Pedido cotizado (PEDCOT), pedido confirmado (PEDCONF), factura (FAC)

        p01 = str(request.query_params.get('p01', '0')).lower()
        p02 = str(request.query_params.get('p02', '%')).lower()
        p03 = str(request.query_params.get('p03', '%')).lower()
        p11 = str(request.query_params.get('p11', '0')).lower()
        p12 = str(request.query_params.get('p12', '2021-01-01'))
        p13 = str(request.query_params.get('p13', '2021-01-31'))
        p15 = str(request.query_params.get('p15', 'COT'))

        pvals = p01 + p02 + p03 + p11 + p12 + p13 + p15

        if pvals == '0%%02021-01-012021-01-31COT':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        if p01 != '0':
            p11 = '0'

        params = [p01, p02, p03, p11, p12, p13, p15]

        result = []

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc('DMC.LINA_QRYSALEDOCSM', params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class SaleDocsDAPIView(APIView):
    """Detalle de documentos de ventas"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - Lista con los números de documentos a consultar
        # p15 - Tipo de documento: Cotización (COT), Pedido cotizado (PEDCOT), pedido confirmado (PEDCONF), factura (FAC)
        
        p01 = str(request.query_params.get('p01', '0')).lower()
        p15 = str(request.query_params.get('p15', 'COT'))

        pvals = p01 + p15

        if pvals == '0COT':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [p01, p15]

        result = []

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc('DMC.LINA_QRYSALEDOCSD', params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class SalesDetailAPIView(APIView):
    """Detalle de ventas"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - Lista de SKUs
        # p02 - Lista de Marcas
        # p03 - Categoría
        # p11 - Tipo de consulta: Listado por números de documentos, por periodo (0, 1)
        # p12 - Fecha inicial del periodo a consultar
        # p13 - Fecha final del periodo a consultar
        # p15 - Tipo de documento: Cotización (COT), Pedido cotizado (PEDCOT), pedido confirmado (PEDCONF), factura (FAC)
        
        p01 = str(request.query_params.get('p01', '0')).lower()
        p02 = str(request.query_params.get('p02', '%')).lower()
        p03 = str(request.query_params.get('p03', '%')).lower()
        p11 = str(request.query_params.get('p11', '0')).lower()
        p12 = str(request.query_params.get('p12', '2021-01-01'))
        p13 = str(request.query_params.get('p13', '2021-01-31'))
        p15 = str(request.query_params.get('p15', 'COT'))

        pvals = p01 + p02 + p03 + p11 + p12 + p13 + p15
        print(pvals)

        if pvals == '0%%02021-01-012021-01-31COT':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        if p01 != '0':
            p11 = '0'
        else:
            p11 = 1

        params = [p01, p02, p03, p11, p12, p13, p15]

        result = []

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc('DMC.LINA_QRYSALESDETAIL', params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class FavoritoModelViewset(CommonViewSet):
    """Vista para CRUD de Favoritos"""

    serializer_class = BIFavoritoSerializer

    queryset = BIFavorito.objects.all()
