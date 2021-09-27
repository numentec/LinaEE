from django.db import connections
from rest_framework import viewsets, status
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers
from ..core.views import CommonViewSet
from ..core.models import SQLQuery

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
        
        p01 = str(request.query_params.get('p01', '0')).lower().strip()
        p02 = str(request.query_params.get('p02', 'BC')).strip()
        p03 = str(request.query_params.get('p03', '01')).strip()

        pvals = p01 + p02 + p03

        if pvals == '0BC01':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [p01, p02, p03]

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

        p01 = str(request.query_params.get('p01', 'sku')).lower().strip()
        p02 = str(request.query_params.get('p02', '0')).strip()
        p03 = str(request.query_params.get('p03', '0')).strip()
        p04 = str(request.query_params.get('p04', '0')).strip()

        pvals = p01 + p02 + p03 + p04

        if pvals == 'sku000':
            return Response([{"status": "NOT EXEC PARAMS"}], status=status.HTTP_200_OK)

        result = []

        qrys = SQLQuery.objects.filter(vista=24)
        qrycalling = qrys[0].content    # 'DMC.LINA_REUBICAR'

        with connections['extdb1'].cursor() as cursor:

            statusmsg = cursor.var(str)

            params = [p01, p02, p03, p04, statusmsg]

            cursor.callproc(qrycalling, params)

            result = [dict({'status': statusmsg.var})]

        return Response(result, status=status.HTTP_200_OK)
