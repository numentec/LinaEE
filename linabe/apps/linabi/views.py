from django.db import connections
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import authentication, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from drf_dx_datagrid import DxModelViewSet
from . import models
from . import serializers
from ..core.views import CommonViewSet
from ..core.models import SQLQuery
from datetime import date

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
    # Vista 19
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - Tipo de lista (CLI, PROV, VEN, MAR, CLA1, CLA2, CLA3, CLAX)

        p01 = str(request.query_params.get('p01', 'X'))

        if p01 == 'X':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        result = []

        query = SQLQuery.objects.get(vista = 19, ordinal = 1)

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            # cursor.callproc('DMC.LINA_LISTS', [p01, refCursor])
            cursor.callproc(query.content, [p01, refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)

class TallasBCAPIView(APIView):
    """Lista de codigo de barras por talla"""
    # Vista 20
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        sku = str(request.query_params.get('sku', 'X')).lower()

        if sku == 'X':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [sku]

        result = []

        query = SQLQuery.objects.get(vista = 20, ordinal = 1)

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            # cursor.callproc('DMC.LINA_TALLASBC', params + [refCursor])
            cursor.callproc(query.content, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class ColoresBCAPIView(APIView):
    """Lista de codigo de barras por color"""
    # Vista 34 -por verificar
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        idVista = 34

        sku = str(request.query_params.get('sku', 'X')).lower()

        if sku == 'X':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [sku]

        result = []

        query = SQLQuery.objects.get(vista = idVista, ordinal = 1)

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            # cursor.callproc('DMC.LINAEE_COLORESBC', params + [refCursor])
            cursor.callproc(query.content, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


# class CatalogModelViewSet(DxModelViewSet):
class CatalogModelViewSet(viewsets.ModelViewSet):
    """Catálogo - Lista de productos"""
    serializer_class = serializers.BICatalogSerializer
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

        qs = ListAsQuerySet(result, model=models.BICatalog)

        return qs


class CatalogAPIView(APIView):
    """Catálogo - Lista de productos"""
    # Vista Nº 14
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        idVista = 14
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
        p01 = str(request.query_params.get('p01', '%')).lower().strip()
        p02 = str(request.query_params.get('p02', '%')).lower().strip()
        p03 = str(request.query_params.get('p03', '%')).lower().strip()
        p04 = str(request.query_params.get('p04', '%')).lower().strip()
        p05 = str(request.query_params.get('p05', '%')).lower().strip()
        p06 = str(request.query_params.get('p06', '%')).lower().strip()
        p07 = str(request.query_params.get('p07', '%')).lower().strip()
        p08 = str(request.query_params.get('p08', '%')).lower().strip()
        p09 = str(request.query_params.get('p09', '%')).lower().strip()
        p10 = str(request.query_params.get('p10', '%')).lower().strip()
        p11 = str(request.query_params.get('p11', 0)).lower()
        p12 = str(request.query_params.get('p12', '2021-01-01')).lower().strip()
        p13 = str(request.query_params.get('p13', '2021-01-01')).lower().strip()
        p14 = str(request.query_params.get('p14', '1')).lower().strip()

        pvals = p01 + p02 + p03 + p04 + p05 + p06 + p07 + p08 + p09 + p10 + p11 + p12 + p13 + p14

        if pvals == '%%%%%%%%%%022021-01-012021-01-011':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14]

        qrys = SQLQuery.objects.filter(vista=idVista)

        result = []
        # qrycalling = 'DMC.LINAEE_QRYCATALOGO'
        qrycalling = qrys[0].content
            
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
            # qrycalling = 'DMC.LINAEE_QRYCATALOGO_SKU'
            qrycalling = qrys[1].content

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

            # Columnas a remover para esta vista y para el grupo del usuario en curso
            colsToRemoveList = request.user.colsToRemoveTmp(idVista)
            # Remueve las columnas indicadas en colsToRemoveList
            result = [{key : val for key, val in sub.items() if key not in colsToRemoveList} for sub in result]

        return Response(result, status=status.HTTP_200_OK)


class StoragexlocAPIView(APIView):
    """Inventario por localización - Lista de productos"""
    # Vista 21
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
        p01 = str(request.query_params.get('p01', '%')).lower().strip()
        p02 = str(request.query_params.get('p02', '%')).lower().strip()
        p03 = str(request.query_params.get('p03', '%')).lower().strip()
        p04 = str(request.query_params.get('p04', '%')).lower().strip()
        p05 = str(request.query_params.get('p05', '%')).lower().strip()
        p06 = str(request.query_params.get('p06', '%')).lower().strip()
        p07 = str(request.query_params.get('p07', '%')).lower().strip()
        p08 = str(request.query_params.get('p08', '%')).lower().strip()
        p09 = str(request.query_params.get('p09', '%')).lower().strip()
        p10 = str(request.query_params.get('p10', '%')).lower().strip()
        p11 = str(request.query_params.get('p11', 0)).lower()
        p12 = str(request.query_params.get('p12', '2021-01-01')).lower().strip()
        p13 = str(request.query_params.get('p13', '2021-01-01')).lower().strip()
        p14 = str(request.query_params.get('p14', '1')).lower().strip()

        pvals = p01 + p02 + p03 + p04 + p05 + p06 + p07 + p08 + p09 + p10 + p11 + p12 + p13 + p14

        if pvals == '%%%%%%%%%%022021-01-012021-01-011':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14]

        qrys = SQLQuery.objects.filter(vista=21)

        result = []
        # qrycalling = 'DMC.LINAEE_QRYCATALOGO'
        qrycalling = qrys[0].content
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
            # qrycalling = 'DMC.LINAEE_QRYCATALOGO_SKU'
            qrycalling = qrys[1].content

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class SaleDocsMAPIView(APIView):
    """Documentos de ventas"""
    # Vista 16
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

        p01 = str(request.query_params.get('p01', '0')).lower().strip()
        p02 = str(request.query_params.get('p02', '%')).lower().strip()
        p03 = str(request.query_params.get('p03', '%')).lower().strip()
        p11 = str(request.query_params.get('p11', '0')).lower().strip()
        p12 = str(request.query_params.get('p12', '2021-01-01')).strip()
        p13 = str(request.query_params.get('p13', '2021-01-31')).strip()
        p15 = str(request.query_params.get('p15', 'COT')).strip()

        pvals = p01 + p02 + p03 + p11 + p12 + p13 + p15

        if pvals == '0%%02021-01-012021-01-31COT':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        if p01 != '0':
            p11 = '0'

        params = [p01, p02, p03, p11, p12, p13, p15]

        result = []

        qrys = SQLQuery.objects.filter(vista=16)
        qrycalling = qrys[0].content    # 'DMC.LINA_QRYSALEDOCSM'

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class SaleDocsDAPIView(APIView):
    """Detalle de documentos de ventas"""
    # Vista 17
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        idVista = 17
        # p01 - Lista con los números de documentos a consultar
        # p15 - Tipo de documento: Cotización (COT), Pedido cotizado (PEDCOT), pedido confirmado (PEDCONF), factura (FAC)
        
        p01 = str(request.query_params.get('p01', '0')).lower().strip()
        p15 = str(request.query_params.get('p15', 'COT')).strip()

        pvals = p01 + p15

        if pvals == '0COT':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [p01, p15]

        result = []

        qrys = SQLQuery.objects.filter(vista=idVista)
        qrycalling = qrys[0].content    # 'DMC.LINA_QRYSALEDOCSD'

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

            # Columnas a remover para esta vista y para el grupo del usuario en curso
            colsToRemoveList = request.user.colsToRemoveTmp(idVista)
            # Remueve las columnas indicadas en colsToRemoveList
            result = [{key : val for key, val in sub.items() if key not in colsToRemoveList} for sub in result]

        return Response(result, status=status.HTTP_200_OK)


class SalesDetailAPIView(APIView):
    """Detalle de ventas por SKU"""
    # Vista 18
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        idVista = 18
        # p01 - Lista de SKUs
        # p02 - Lista de Marcas
        # p03 - Categoría
        # p11 - Tipo de consulta: Listado por lista de SKUs, por periodo (0, 1)
        # p12 - Fecha inicial del periodo a consultar
        # p13 - Fecha final del periodo a consultar
        # p15 - Tipo de documento: Cotización (COT), Pedido cotizado (PEDCOT), pedido confirmado (PEDCONF), factura (FAC)
        
        p01 = str(request.query_params.get('p01', '0')).lower().strip()
        p02 = str(request.query_params.get('p02', '%')).lower().strip()
        p03 = str(request.query_params.get('p03', '%')).lower().strip()
        p11 = str(request.query_params.get('p11', '0')).lower().strip()
        p12 = str(request.query_params.get('p12', '2021-01-01')).strip()
        p13 = str(request.query_params.get('p13', '2021-01-31')).strip()
        p15 = str(request.query_params.get('p15', 'COT')).strip()

        pvals = p01 + p02 + p03 + p11 + p12 + p13 + p15
        print(pvals)

        if pvals == '0%%02021-01-012021-01-31COT':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        if p01 != '0':
            p11 = 0
        else:
            p11 = 1

        # Preparar lista de SKUs o codigos de barra
        if (',' in p01):
            p01 = p01.replace(' ', '')
        elif (' ' in p01):
            p01 = p01.replace(' ', ',')

        params = [p01, p02, p03, p11, p12, p13, p15]

        result = []

        qrys = SQLQuery.objects.filter(vista=idVista)
        qrycalling = qrys[0].content

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

            # Columnas a remover para esta vista y para el grupo del usuario en curso
            colsToRemoveList = request.user.colsToRemoveTmp(idVista)
            # Remueve las columnas indicadas en colsToRemoveList
            result = [{key : val for key, val in sub.items() if key not in colsToRemoveList} for sub in result]

        return Response(result, status=status.HTTP_200_OK)


class BIQueryModelViewset(CommonViewSet):
    """Vista para CRUD de BIQuery"""
    # Vista 22
    serializer_class = serializers.BIQuerySerializer

    queryset = models.BIQuery.objects.filter(is_active = True)


class FavoritoModelViewset(CommonViewSet):
    """Vista para CRUD de Favoritos"""
    # Vista 15
    serializer_class = serializers.BIFavoritoSerializer

    queryset = models.BIQuery.objects.filter(is_active = True, favoritos = True)


class BIXLSXTemplateModelViewset(CommonViewSet):
    """Vista para CRUD de BIXLSXTemplate"""
    serializer_class = serializers.BIXLSXTemplateSerializer

    queryset = models.BIXLSXTemplate.objects.all()


class BIXLSXTemplateColModelViewset(CommonViewSet):
    """Vista para CRUD de BIXLSXTemplateCol"""
    serializer_class = serializers.BIXLSXTemplateColSerializer

    queryset = models.BIXLSXTemplateCol.objects.all()


class BIDashboardExt(APIView):
    """Consultas externas para el Dashboard de Lina BI"""
    # Vista 31
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - Switch par seleccionar consulta
        # p02 - Cia en curso
        # p03 - Fecha inicial del periodo a consultar
        # p04 - Fecha final del periodo a consultar
        # p05 - Filtro adicional para el tipo de marca (Marca externa)
        # p06 - Cantidad de registros a recuperar (SQL LIMIT)


        p01 = str(request.query_params.get('p01', '1')).lower().strip()
        p02 = str(request.query_params.get('p02', '01')).lower().strip()
        p03 = str(request.query_params.get('p03', '2022-01-01')).strip()
        p04 = str(request.query_params.get('p04', '2022-03-31')).strip()
        p05 = str(request.query_params.get('p05', 'false')).strip()
        p06 = str(request.query_params.get('p06', '1000')).strip()
        

        pvals = p01 + p02 + p03 + p04 + p05 + p06

        if pvals == '1012022-01-012022-03-31false1000':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        qrys = SQLQuery.objects.filter(vista=31)

        # Preparar parametros
        if p01 != '0':
            params = [p01, p02, p03, p04, p05, p06]
            qrycalling = qrys[0].content
        else:
            params = [p02, p03, p04, p05]
            qrycalling = qrys[1].content

        result = []

        with connections['extdb1'].cursor() as cursor:

            if p01 != '0':
                if p01 == '13':
                    # refCursor = cursor.connection.cursor()

                    # #cursor.callproc(qrycalling, params + [refCursor] + [p05])
                    # oxqry = """
                    # SELECT ROWNUM AS ID, T1.* FROM (SELECT REFERENCIA AS SKU, DESCRIPCION AS DESCRIP, ABREVIATURA AS UM,
                    # CANT_VENDIDA AS CANTIDAD, NVL(PRECIO_VENTA, 0) AS PRECIO, NVL(FACTURA_TOTAL, 0) AS MONTO, CLIENTE, 
                    # NOMBRE_CLIENTE AS NOMCLI, NOM_VENDEDOR AS VENDEDOR, FECHA_FACTURA AS FECHA, NU_FACTURA_COMERCIAL AS IDDOC
                    # FROM DMC.LINAEE_DET_FACTURA_VW WHERE FECHA_FACTURA > TO_DATE(SYSDATE - 2) ORDER BY FECHA_FACTURA DESC,
                    # NU_FACTURA_COMERCIAL DESC) T1 WHERE ROWNUM <= 12"""
                    # #oxqry = oxqry1 + oxqry2 + oxqry3 + oxqry4 + oxqry5
                    # cursor.execute(oxqry)

                    # descrip = refCursor.description

                    # rows = refCursor.fetchall()

                    # result = [dict(zip([column[0] for column in descrip], row)) for row in rows]
                    result = []
                else:
                    refCursor = cursor.connection.cursor()

                    cursor.callproc(qrycalling, params + [refCursor])

                    descrip = refCursor.description

                    rows = refCursor.fetchall()

                    result = [dict(zip([column[0] for column in descrip], row)) for row in rows]
            else:
                r1 = cursor.var(float).var
                r2 = cursor.var(float).var
                r3 = cursor.var(float).var

                cursor.callproc(qrycalling, params + [r1, r2, r3] )

                result = [dict({'V1': r1.getvalue(), 'V2': r2.getvalue(), 'V3': r3.getvalue()})]

        return Response(result, status=status.HTTP_200_OK)

class CxCAntigAPIView(APIView):
    """Cuentas por cobrar por Antigüedad"""
    # Vista 32
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        idVista = 32
        # p01 - ID de compañía %
        # p12 - Fecha de inicio del periodo a analizar
        # p13 - Fecha hasta donde se quiere analizar la antigüedad <Date>
        p01 = str(request.query_params.get('p01', '%')).lower().strip()
        p12 = str(request.query_params.get('p12', '0')).lower().strip()
        p13 = str(request.query_params.get('p13', '0')).lower().strip()

        pvals = p01 + p12 + p13

        if pvals == '%00':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        if p12 == '0':
            p12 = date.today()

        if p13 == '0':
            p13 = date.today()

        params = [p01, p12, p13]

        qrys = SQLQuery.objects.filter(vista=idVista)

        result = []
        # qrycalling = 'DMC.LINAEE_CXCANTIG'
        qrycalling = qrys[0].content

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

            # Columnas a remover para esta vista y para el grupo del usuario en curso
            colsToRemoveList = request.user.colsToRemoveTmp(idVista)
            # Remueve las columnas indicadas en colsToRemoveList
            result = [{key : val for key, val in sub.items() if key not in colsToRemoveList} for sub in result]

        return Response(result, status=status.HTTP_200_OK)


class BICustomCatalogMasterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing BICustomCatalogMaster.
    The serializer already includes the details associated with each custom catalog.
    """
    # Vista 37
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = models.BICustomCatalogMaster.objects.all()
    serializer_class = serializers.BICustomCatalogMasterSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'created_ad', 'status', 'created_by__username', 'customer_name']
    ordering_fields = ['id', 'created_at', 'status', 'created_by__username', 'customer_name']

    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


class BICustomCatalogMasterOnlyViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing BICustomCatalogMaster.
    The serializer already includes the details associated with each custom catalog.
    """
    # Vista 38
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = models.BICustomCatalogMaster.objects.all()
    serializer_class = serializers.BICustomCatalogMasterOnlySerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'created_ad', 'status', 'created_by__username', 'customer_name']
    ordering_fields = ['id', 'created_at', 'status', 'created_by__username', 'customer_name']

    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)