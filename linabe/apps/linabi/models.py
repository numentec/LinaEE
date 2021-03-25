from django.db import models
from .attributs import attrs_catalog
from ..core.models import Common


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
