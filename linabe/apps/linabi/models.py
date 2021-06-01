import os
from django.db import models
from .attributs import attrs_catalog
from ..core.models import Common


# Se asegura que el nombre de archivo de la plantilla
# coincida con el campo "name" asignado por el usuario
def template_path(instance, filename):
    """Se asegura que el nombre de archivo de la plantilla
    coincida con el campo "name" asignado por el usuario"""
    ext = filename.split('.')[-1]
    onlyname = getattr(instance, 'name').lower()
    filename = f'{onlyname}.{ext}'

    return os.path.join('xlsxtemplates/', filename)


# Clase base abstracta para modelo transitorio.
class TransientModel(models.Model):
    """Inherit from this class to use
     django constructors and serialization
     but no database management
    """
    def save(*args, **kwargs):
        pass  # avoid exceptions if called

    class Meta:
        abstract = True  # no table for this class
        managed = False  # no database management

# Modelo transitorio para cargar productos (extdb1)
BICatalog = type("BICatalog", (TransientModel,), attrs_catalog)

# Modelo para enlaces a favoritos
class BIFavorito(Common):
    """Modelo para favoritos en LinaBI"""
    name = models.CharField("Nombre", max_length=25, unique=True)
    link = models.CharField("Enlace", max_length=200, unique=True)
    descrip = models.TextField("Descripción", blank = True)
    todos = models.BooleanField("Todos", default=True)
    vuextore = models.CharField("Vuex Store", max_length=50, blank=True)
    image = models.ImageField('Imagen', upload_to='images/bifavoritos', \
         blank=True, default='images/bifavoritos/prev1.jpg')

    class Meta:
        db_table = 'linabi_favorito'
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str_(self):
        return "Reporte {}".format(self.name)


# Modelo para plantillas de Excel
class BIXLSXTemplate(Common):
    """Modelo para plantillas xlsx en LinaBI"""
    name = models.CharField("Nombre", max_length=10, unique=True)
    descrip = models.TextField("Descripción", blank = True)
    row = models.IntegerField("Fila Inicial", default=1)
    col = models.IntegerField("Columna Inicial", default=1)
    archivo = models.FileField('Archivo xlsx', upload_to=template_path)

    class Meta:
        db_table = 'linabi_xlsxtemplate'
        verbose_name = 'Plantilla xlsx'
        verbose_name_plural = 'Plantillas xlsx'

    def __str_(self):
        return "Plantilla {}".format(self.name)

# Modelo para columnas incluidas en la plantilla de Excel
class BIXLSXTemplateCol(Common):
    """Modelo para columnas incluidas en la plantilla xlsx en LinaBI"""
    name = models.CharField("Columna", max_length=20, unique=True)
    descrip = models.TextField("Descripción", blank = True)
    orden = models.IntegerField("Orden", default=0)
    posicion = models.IntegerField("Posición", default=1)
    plantilla = models.ForeignKey(BIXLSXTemplate, on_delete=models.CASCADE, \
                verbose_name='Plantilla', related_name='cols_x_plantilla')

    class Meta:
        db_table = 'linabi_xlsxtemplatecol'
        verbose_name = 'Columna'
        verbose_name_plural = 'Columnas'

    def __str_(self):
        return "Columna {}".format(self.name)