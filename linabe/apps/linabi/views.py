from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import connection
import cx_Oracle 

class TestApiView(APIView):
    """Test API View"""

    def get(self, request, format=None):
        """Returns a list of APIView features"""

        # print(con.version)
        
        # con.close() 

        # query = 'SELECT * FROM lina_core_stakeholders WHERE is_cli'
        query = 'SELECT * FROM DMC.LINA_DISTRO_TALLAS WHERE ROWNUM <= 1000'

        try:
            # cursor = connection.cursor()
            conn = cx_Oracle.connect('pocket/qazwsx12@201.218.202.43:1522/vertigo') 
            cursor = conn.cursor()
            cursor.execute(query)
            descrip = cursor.description

            rows = cursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]
        finally:
            cursor.close()
            # conn.close()

        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]

        return Response(result, status=status.HTTP_200_OK)
