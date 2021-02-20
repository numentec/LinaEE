from django.db import models, connections

class ListAsQuerySet(list):

    def __init__(self, *args, model, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self  # filter ignoring, but you can impl custom filter

    def order_by(self, *args, **kwargs):
        return self


class LinaBIManager(models.Manager):

    def raw_as_qs(self, raw_query, params=(), translations={}):

        qs = self.get_queryset()
        return qs.raw(raw_query, params, translations)

    def cur_as_qs(self, raw_query, params=[], exec_type=1):

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            if exec_type == 1:
                cursor.callproc(raw_query, params + [refCursor])
            else:
                cursor.execute(raw_query, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return result
