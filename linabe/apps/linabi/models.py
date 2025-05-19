import os
import secrets
from datetime import date, timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from .attributs import attrs_catalog
from ..core.models import Common, StakeHolder

LinaUserModel = get_user_model()


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


# Modelo para enlaces a consultas de LinaBI
class BIQuery(Common):
    """Modelo para consultas en LinaBI"""
    QTYPES_CHOICES = [
        ('qry', 'Query'),
        ('rpt', 'Report'),
        ('tool', 'Tool'),
        ('dbel', 'Dashboard Element'),
    ]

    name = models.CharField("Nombre", max_length=25, unique=True)
    link = models.CharField("Enlace", max_length=200, default='/')
    param = models.CharField("Parámetro", max_length=10, blank=True)
    descrip = models.TextField("Reseña", blank = True)
    qdescrip = models.CharField("Descripción", max_length=30, blank = True)
    owner  = models.ForeignKey(LinaUserModel, null=True, db_index=True, verbose_name='Owner',
                on_delete=models.SET_NULL, related_name='biqueries_x_owner')
    todos = models.BooleanField("Todos", default=True)
    vuextore = models.CharField("Vuex Store", max_length=50, blank=True)
    image = models.ImageField('Imagen', upload_to='images/bifavoritos', \
         blank=True, default='images/bifavoritos/prev1.jpg')
    qtype = models.CharField('Tipo', max_length=4, choices=QTYPES_CHOICES, default='qry')
    favoritos = models.BooleanField('Favoritos', default=False)
    perm = models.CharField("Permiso", max_length=50, blank = True, help_text='Permiso de acceso relacionado')

    class Meta:
        db_table = 'linabi_query'
        verbose_name = 'BIQuery'
        verbose_name_plural = 'BIQueries'

    def __str_(self):
        return "BI Query {}".format(self.name)


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
    perm = models.CharField("Permiso", max_length=50, blank = True, help_text='Permiso de acceso relacionado')

    class Meta:
        db_table = 'linabi_favorito'
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str_(self):
        return "Reporte {}".format(self.name)


# Se asegura que el nombre de archivo de la plantilla
# coincida con el campo "name" asignado por el usuario
def template_path(instance, filename):
    """Se asegura que el nombre de archivo de la plantilla
    coincida con el campo "name" asignado por el usuario"""
    ext = filename.split('.')[-1]
    onlyname = getattr(instance, 'name').lower()
    filename = f'{onlyname}.{ext}'

    return os.path.join('plantillas/', filename)

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
    name = models.CharField("Columna", max_length=20)
    descrip = models.TextField("Descripción", blank = True)
    ordinal = models.IntegerField("Ordinal", default=0)
    posicion = models.IntegerField("Posición", default=1)
    plantilla = models.ForeignKey(BIXLSXTemplate, on_delete=models.CASCADE, \
                verbose_name='Plantilla', related_name='cols_x_plantilla')

    class Meta:
        db_table = 'linabi_xlsxtemplatecol'
        verbose_name = 'Columna'
        verbose_name_plural = 'Columnas'

    def __str_(self):
        return "Columna {}".format(self.name)


# Modelo para categorías temporales de los usuarios 
class BICustomCatalogCategory(Common):
    """Modelo para categorías alternativas temporales creadas por usuarios"""
    name = models.CharField("Nombre", max_length=20)
    descrip = models.TextField("Descripción", blank = True)

    class Meta:
        unique_together = ('name', 'created_by',)
        db_table = 'linabi_customcatalogcat'
        verbose_name = 'Custom Category'
        verbose_name_plural = 'Custom Categories'

def defaultTTL():
    return timezone.now() + timedelta(days=5)

def genToken():
    return secrets.token_urlsafe(32)


# Modelo para maestro de catálogo personalizado
class BICustomCatalogMaster(Common):
    """Modelo para maestro de catálogo personalizado"""
    name = models.CharField("Nombre", max_length=20, blank=True, default='Custom Catalog')
    descrip = models.TextField("Descripción", blank = True)
    note =  models.TextField("Nota", blank = True)
    token = models.CharField("Token", max_length=45, unique=True, default=genToken)
    ttl = models.DateField("TTL", default=defaultTTL)
    customer_name = models.CharField("Nombre del Cliente", max_length=100, blank=True)
    customer_email = models.EmailField("Email del Cliente", max_length=100, blank=True)
    customer_phone = models.CharField("Teléfono del Cliente", max_length=50, blank=True)
    salesperson = models.ForeignKey(LinaUserModel, on_delete=models.SET_NULL, \
                verbose_name='Vendedor', related_name='catalogs_as_salesperson', null=True)
    stakeholder = models.ForeignKey(StakeHolder, on_delete=models.SET_NULL, \
                verbose_name='Cliente', related_name='catalogs_as_stakeholder', null=True)

    def save(self, *args, **kwargs):
        if not self.salesperson and self.created_by:
            self.salesperson = self.created_by
        super(BICustomCatalogMaster, self).save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     if not self.ttl:
    #         self.ttl = defaultTTL()
    #     super(BICustomCatalogMaster, self).save(*args, **kwargs)

    class Meta:
        db_table = 'linabi_customcatalogm'
        verbose_name = 'Catalogo'
        verbose_name_plural = 'Catalogos'

    def __str_(self):
        return "Custom catalog {} / {}".format(self.name, self.token)


# Modelo para detalle de catálogo personalizado
class BICustomCatalogDetail(Common):
    """Modelo para detalle de catálogo personalizado"""
    sku = models.CharField("SKU", max_length=50)
    note =  models.TextField("Nota", blank = True)
    price = models.DecimalField("Precio", max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField("Stock", default=0)
    category = models.ForeignKey(BICustomCatalogCategory, on_delete=models.SET_NULL, null=True)
    catalog =  models.ForeignKey(BICustomCatalogMaster, on_delete=models.CASCADE)

    class Meta:
        db_table = 'linabi_customcatalogd'
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'

    def __str_(self):
        return "Item {} - {} - {}".format(self.id, self.sku, self.catalog)


# Ruta de las imágenes de un custom catalog específico
def cc_path(instance, filename):
    """Ruta de las imágenes de un custom catalog específico"""
    itemd = getattr(instance, 'itemdetail')
    ccdir = 'cc' + str(itemd.catalog.id) + '/'

    return os.path.join('images/customcatalogs/', ccdir + filename)

# Modelo para imágenes adicionales para cada item del detalle de catálogo personalizado
class BICustomCatalogDetailImage(models.Model):
    """Modelo para imágenes adicionales para items del detalle de catálogo personalizado"""
    itemdetail = models.ForeignKey(BICustomCatalogDetail, on_delete=models.CASCADE)
    image = models.ImageField('Imagen', upload_to=cc_path, blank=True)

    class Meta:
        db_table = 'linabi_customcatalogdimg'
        verbose_name = 'Custom Catalog Image'
        verbose_name_plural = 'Custom Catalogs Images'

