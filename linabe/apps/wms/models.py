from django.db import models
from django.contrib.auth import get_user_model
from ..core.models import Common

LinaUserModel = get_user_model()

# Modelo para enlaces a consultas de WMS
class WMSQuery(Common):
    QTYPES_CHOICES = [
        ('qry', 'Query'),
        ('rpt', 'Report'),
        ('tool', 'Tool'),
    ]

    """Modelo para consultas en WMS"""
    name = models.CharField("Nombre", max_length=25, unique=True)
    link = models.CharField("Enlace", max_length=200, default='/')
    param = models.CharField("Parámetro", max_length=10, blank=True)
    descrip = models.TextField("Reseña", blank = True)
    qdescrip = models.CharField("Descripción", max_length=30, blank = True)
    owner  = models.ForeignKey(LinaUserModel, null=True, db_index=True, verbose_name='Owner',
                on_delete=models.SET_NULL, related_name='wmsqueries_x_owner')
    todos = models.BooleanField("Todos", default=True)
    vuextore = models.CharField("Vuex Store", max_length=50, blank=True)
    image = models.ImageField('Imagen', upload_to='images/bifavoritos', \
         blank=True, default='images/bifavoritos/prev1.jpg')
    favoritos = models.BooleanField('Favoritos', default=False)
    perm = models.CharField("Permiso", max_length=50, blank = True, help_text='Permiso de acceso relacionado')
    qtype = models.CharField('Query type', max_length=5, choices=QTYPES_CHOICES, default='qry')

    class Meta:
        db_table = 'wms_query'
        verbose_name = 'WMSQuery'
        verbose_name_plural = 'WMSQueries'

    def __str_(self):
        return "WMS Query {}".format(self.name)
