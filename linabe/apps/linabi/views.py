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
    def __init__(self, *args, model, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self  # filter ignoring, but you can impl custom filter

    def order_by(self, *args, **kwargs):
        return self


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

        p01 = str(request.query_params.get('p01', '%')).lower()
        p02 = str(request.query_params.get('p02', 'camisa%')).lower()
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

        params = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14]

        result = []

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc('DMC.LINA_QRYCATALOGO', params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class SaleDocsMAPIView(APIView):
    """Documentos de Ventas"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - Lista con los números de documentos a consultar
        # p02 - Nombre del cliente
        # p11 - Tipo de consulta: Listado por números de documentos, por periodo (0, 1)
        # p12 - Fecha inicial del periodo a consultar
        # p13 - Fecha final del periodo a consultar
        # p15 - Tipo de documento: Cotización (COT), Pedido cotizado (PEDCOT), pedido confirmado (PEDCONF), factura (FAC)
        
        p01 = str(request.query_params.get('p01', '0')).lower()
        p02 = str(request.query_params.get('p02', '%')).lower()
        p11 = str(request.query_params.get('p11', '1')).lower()
        p12 = str(request.query_params.get('p12', '2021-01-01'))
        p13 = str(request.query_params.get('p13', '2021-01-31'))
        p15 = str(request.query_params.get('p15', 'COT'))

        # pvals = p01 + p02 + p11 + p12 + p13 + p15

        # if pvals == '0%022021-01-012021-01-31COT':
        #     return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        if p01 != '0':
            p11 = '0'

        params = [p01, p02, p11, p12, p13, p15]

        result = []

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc('DMC.LINA_QRYSALEDOCSM', params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class FavoritoModelViewset(CommonViewSet):
    """Vista para CRUD de Favoritos"""

    serializer_class = BIFavoritoSerializer

    queryset = BIFavorito.objects.all()
