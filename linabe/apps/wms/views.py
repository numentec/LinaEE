from django.db import connections
from django.http import response
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers
from ..core.views import CommonViewSet
from ..core.models import SQLQuery

import json, uuid

LinaUserModel = get_user_model()

def curUser(usr):
    return LinaUserModel.objects.get(username = usr)


class WMSQueryModelViewset(CommonViewSet):
    """Vista para CRUD de WMSQuery"""
    # Vista 23
    serializer_class = serializers.WMSQuerySerializer

    queryset = models.WMSQuery.objects.all()

    def list(self, request):
        qtype = request.query_params.get('qtype')
        only_actives = request.query_params.get('only_actives')

        if only_actives:
            if qtype == 'all':
                queryset = models.WMSQuery.objects.filter(is_active = True)
            else:
                queryset = models.WMSQuery.objects.filter(is_active = True, qtype = qtype)
        else:
            if qtype != 'all':
                queryset = models.WMSQuery.objects.filter(qtype = qtype)

        serializer = self.get_serializer(queryset, many=True)
        resultset = serializer.data

        return Response(resultset)


class WMSToolsModelViewset(CommonViewSet):
    """Vista para CRUD de WMSQuery"""
    # Vista XX
    serializer_class = serializers.WMSQuerySerializer

    queryset = models.WMSQuery.objects.filter(is_active = True, qtype = 'tool')


class QryStockExtAPIView(APIView):
    """Consultar stock por ubicación (data externa)"""
    # Vista 24
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - Código de barra o SKU
        # p02 - Tipo de dato (BC o SKU)
        # p03 - Compañía
        # p04 - D = Disponible / T = Todo
        
        p01 = str(request.query_params.get('p01', '0')).lower().strip()
        p02 = str(request.query_params.get('p02', 'BC')).strip()
        p03 = str(request.query_params.get('p03', '01')).strip()
        p04 = str(request.query_params.get('p04', 'T')).strip()

        pvals = p01 + p02 + p03 + p04

        if pvals == '0BC01T':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)


        params = [p01, p02, p03, p04]

        result = []

        qrys = SQLQuery.objects.filter(vista=24)
        qrycalling = qrys[0].content    # 'DMC.LINA_QRYSTOCKXLOC'

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class RelocateExtAPIView(APIView):
    """Reubicar producto en bodega (data externa)"""
    # Vista 25
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - SKU
        # p02 - ID de ubicación origen
        # p03 - ID de ubicación destino
        # p04 - Cantidad a reubicar
        # p05 - CIA

        p01 = str(request.query_params.get('p01', 'sku')).lower().strip()
        p02 = str(request.query_params.get('p02', '0')).strip()
        p03 = str(request.query_params.get('p03', '0')).strip()
        p04 = str(request.query_params.get('p04', '0')).strip()
        p05 = str(request.query_params.get('p05', '01')).strip()

        pvals = p01 + p02 + p03 + p04 + p05

        if pvals == 'sku00001':
            return Response([{"status": "NOT EXEC PARAMS"}], status=status.HTTP_200_OK)

        usr = request.user.username
        usr_extrel = request.user.extrel

        result = []

        qrys = SQLQuery.objects.filter(vista=25)
        qrycalling = qrys[0].content    # 'DMC.LINA_REUBICAR'

        with connections['extdb1'].cursor() as cursor:

            statusmsg = cursor.var(str).var

            params = [p01, p02, p03, p04, p05, usr, usr_extrel, statusmsg]

            cursor.callproc(qrycalling, params)

            result = [dict({'status': statusmsg.getvalue()})]

        return Response(result, status=status.HTTP_200_OK)


class QryOneProdAPIView(APIView):
    """Consultar un producto por SKU o código de barra"""
    # Vista Nº 26
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - SKU o código de barra exactos
        # p02 - Tipo de consulta (SKU o BC)
        # p03 - Compañía
        p01 = str(request.query_params.get('p01', '0')).lower().strip()
        p02 = str(request.query_params.get('p02', 'SKU')).strip()
        p03 = str(request.query_params.get('p03', '00')).lower().strip()

        pvals = p01 + p02 + p03

        if pvals == '0SKU00':
            return Response([{"RESULT": "NO PARAMS"}], status=status.HTTP_200_OK)

        params = [p01, p02, p03]

        qrys = SQLQuery.objects.filter(vista=26)

        result = []
        #qrycalling = 'DMC.LINAEE_PROD_BY_SKU'
        qrycalling = qrys[0].content

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)

class ProdsPerLocAPIView(APIView):
    """Productos en una ubicación dada"""
    # Vista 28
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - Código de barra de la ubicación (BINLOCATION)
        # p02 - Tipo de dato (BC o CODIGO)
        # p03 - Compañía

        p01 = str(request.query_params.get('p01', '0')).lower().strip()
        p02 = str(request.query_params.get('p02', 'BC')).strip()
        p03 = str(request.query_params.get('p03', '01')).strip()

        pvals = p01 + p02 + p03

        if pvals == '0BC01':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [p01, p02, p03]

        result = []

        # qrys = SQLQuery.objects.filter(vista=27)
        # qrycalling = qrys[0].content    # 'DMC.LINAEE_PRODSXLOC'
        qrycalling = 'DMC.LINAEE_PRODSXLOC'

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class ProdsPerMarbeteAPIView(APIView):
    """Productos (SKU) señalados por un mismo marbete"""
    # Vista 29
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # p01 - Número de marbete (BINLOCATION)
        # p02 - Tipo de dato (BC o CODIGO)
        # p03 - Compañía

        p01 = str(request.query_params.get('p01', '0')).lower().strip()
        p02 = str(request.query_params.get('p02', 'BC')).strip()
        p03 = str(request.query_params.get('p03', '01')).strip()

        pvals = p01 + p02 + p03

        if pvals == '0BC01':
            return Response([{"msg": "NO DATA"}], status=status.HTTP_200_OK)

        params = [p01, p02, p03]

        result = []

        # qrys = SQLQuery.objects.filter(vista=27)
        # qrycalling = qrys[0].content    # 'DMC.LINAEE_PRODSXMARBETE'
        qrycalling = 'DMC.LINAEE_PRODSXMARBETE'

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class ExtCountedProdsAPIView(APIView):
    """Insertar cuenta de Productos en DB externa"""
    # Vista 30
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # items - Registros a insertar
        # cia - Compañía
        usr = curUser(request.user)

        try:
            data = request.data

            if not data:
                return Response({"msg": "WARNING: NO DATA HAS BEEN SENT"}, status=status.HTTP_200_OK)

            items = data['items']
            cia = data['cia']

            items_list = json.loads(items)

            sessionID = uuid.uuid4().hex

            data_set = []
            for item in items_list:
                data_set.append(
                    [
                        cia,
                        usr.extrel,
                        sessionID,
                        item['NUMINV'],
                        item['MARBETE'],
                        item['SKU'],
                        item['PACKAGE'],
                        item['PACKING'],
                        item['PACKINGTOT'],
                        item['UNI'],
                        item['MULTIPLO'],
                        item['UBIX'],
                        item['UBIXBC'],
                        item['CTIME'],
                    ])

            with connections['extdb1'].cursor() as cursor:

                refCursor = cursor.connection.cursor()
                    
                refCursor.executemany(
                    "INSERT INTO DMC.LINAEE_CONTEO VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14)",
                    data_set
                )

            response =  Response({"msg": "Conteo enviado con éxito"}, status=status.HTTP_200_OK)

        except Exception as exc:
            response = self.handle_exception(exc)

        return response

