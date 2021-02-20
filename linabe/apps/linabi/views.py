from rest_framework import viewsets
from .models import BICatalog
from django.db import connections
from .serializers import BICatalogSerializer
from drf_dx_datagrid import DxModelViewSet

class ListAsQuerySet(list):

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

        params = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14]

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc('DMC.LINA_QRYCATALOGO', params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        qs = ListAsQuerySet(result, model=BICatalog)

        return qs
