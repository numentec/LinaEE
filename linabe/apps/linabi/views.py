from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import BICatalog
from .serializers import BICatalogSerializer
from django.db import connections
import cx_Oracle 

class TestApiView(APIView):
    """Test API View"""

    def get(self, request, format=None):
        """Returns a list of APIView features"""

        # print(con.version)
        
        # con.close() 

        # query = 'SELECT * FROM lina_core_stakeholders WHERE is_cli'
        query = 'SELECT * FROM DMC.LINA_DISTRO_TALLAS WHERE ROWNUM <= 1000'
        result = []

        with connections['extdb1'].cursor() as cursor:
        # with cx_Oracle.connect('pocket/qazwsx12@201.218.202.43:1522/vertigo').cursor() as cursor:
            cursor.execute(query)
            descrip = cursor.description

            rows = cursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class TestApiView2(ListAPIView):
    """Lista de distros"""
    serializer_class = BICatalogSerializer

    def get_queryset(self):
        name_map = {'rownum': 'id', 'referencia': 'sku', 'distro': 'distro'}
        return BICatalog.objects.raw('SELECT rownum, t.* FROM DMC.LINA_DISTRO_TALLAS t WHERE ROWNUM <= 1000', \
            translations=name_map)