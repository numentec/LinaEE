from django.db import connections
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework import status
from ..core.models import SQLQuery


class CategoryBrandListAPIView(APIView):
    """ Devuelve la lista de Departamentos (DEPTO), Categorías (CAT) o Subcategorías (SUBCAT)
        Junto con las marcas asociadas a cada una de ellas.
        Parámetros: p01, p02
        p01 - Tipo de lista (DEPTO, CAT, SUBCAT)
        p02 - Company
        La lista que se devuelve depende del valor del parámetro que se pase a la consulta (p01).
        Por ejemplo, si p01 = 'DEPTO', se devolverá la lista de departamentos con las marcas asociadas a cada uno de ellos.
        Si p01 = 'CAT', se devolverá la lista de categorías con las marcas asociadas a cada una de ellas.
        Si p01 = 'SUBCAT', se devolverá la lista de subcategorías con las marcas asociadas a cada una de ellas.
        Si p01 = 'X', se devolverá un mensaje de error.
    """
    # Vista 35
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        idVista = 35
        # p01 - Tipo de lista (DEPTO, CAT, SUBCAT)
        # p02 - Company

        p01 = str(request.query_params.get('p01', 'X'))
        p02 = str(request.query_params.get('p02', '01'))

        if p01 == 'X':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [p01, p02]

        qrys = SQLQuery.objects.filter(vista=idVista)

        result = []
        # qrycalling = 'DMC.LINAEE_CATSBRANDS'
        qrycalling = qrys[0].content
        
        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)
