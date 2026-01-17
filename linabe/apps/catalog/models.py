import os
import secrets
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from ..core.models import Common, Customer, Cia

LinaUserModel = get_user_model()


def defaultTTL():
    """Función para establecer un valor por defecto para el campo TTL
    que es la fecha de expiración del catálogo 
    por defecto es 5 días a partir de la fecha actual
    """
    return (timezone.now() + timedelta(days=5)).date()

def genToken():
    """Genera un token único para el catálogo
    El token es una cadena aleatoria de 32 caracteres alfanuméricos
    Utiliza token_urlsafe para generar un token que sea seguro para URLs
    """
    return secrets.token_urlsafe(32)

def catalog_path(instance, filename):
    """Define la ruta de las imágenes de un item de catálogo
    La ruta se construye con el ID del item del catálogo para mantener las imágenes organizadas
    """
    itemd = getattr(instance, 'itemdetail')
    cpath = 'cp' + str(itemd.catalog.id) # + '/'

    return os.path.join('images/catalogs/', cpath, filename)


class Category(Common):
    """Modelo para categorías de catálogo
    Este modelo permite crear una jerarquía de categorías para organizar los detalles del catálogo.
    Cada categoría puede tener un padre, lo que permite crear subcategorías.
    """
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    description = models.TextField(blank=True, null=True)
    ext_related_id = models.CharField("ID Externo", max_length=100, blank=True, null=True)
    image = models.ImageField("Imagen", upload_to='images/categories/', blank=True, null=True)
    
    # Relación con Cia - Una categoría puede estar disponible para múltiples compañías
    available_for_companies = models.ManyToManyField(
        Cia,
        verbose_name="Disponible para Compañías",
        related_name='available_categories',
        blank=True,
        help_text="Selecciona las compañías para las cuales esta categoría está disponible"
    )

    def __str__(self):
        return self.name

    def get_ancestors(self):
        """Devuelve una lista de ancestros desde el padre hasta la raíz."""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors
    
    def is_available_for_company(self, company):
        """Verifica si la categoría está disponible para una compañía específica."""
        if not self.available_for_companies.exists():
            # Si no hay compañías asignadas, está disponible para todas
            return True
        return self.available_for_companies.filter(id=company.id).exists()
    
    def get_available_companies(self):
        """Devuelve las compañías para las cuales está disponible esta categoría."""
        return self.available_for_companies.all()
    
    class Meta:
        # db_table = 'catalog_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Tag(Common):
    """Modelo para etiquetas personalizadas creadas por usuarios
    Este modelo permite a los usuarios crear etiquetas que pueden ser
    asignadas a los detalles del catálogo para una mejor organización y búsqueda.
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'catalog_tag'
        verbose_name = 'Custom Tag'
        verbose_name_plural = 'Custom Tags'


class CatalogMaster(Common):
    """Modelo para maestro de catálogo"""
    company_id = models.CharField(max_length=32, default='01')
    owner = models.ForeignKey(
        LinaUserModel,
        on_delete=models.CASCADE,
        related_name="catalogs",
    )
    name = models.CharField("Nombre", max_length=20, blank=True, default='Custom Catalog')
    descrip = models.TextField("Descripción", blank = True)
    note =  models.TextField("Nota", blank = True, default='No additional notes')
    token = models.CharField("Token", max_length=45, unique=True, default=genToken)
    ttl = models.DateField("TTL", default=defaultTTL)
    seller = models.ForeignKey(LinaUserModel, on_delete=models.SET_NULL, \
             verbose_name='Vendedor', related_name='catalogs_by_seller', null=True)
    customer = models.ManyToManyField(Customer, verbose_name='Customer', \
                  related_name='catalogs_by_customer', blank=True)
    template = models.CharField(max_length=32, default="Minimal")
    orientation = models.CharField(
        max_length=16,
        choices=(("portrait", "portrait"), ("landscape", "landscape")),
        default="portrait",
    )

    # JSON "source of truth"
    settings = models.JSONField(default=dict, blank=True)
    theme = models.JSONField(default=dict, blank=True)
    pages = models.JSONField(default=list, blank=True)

    share_token = models.CharField(
        max_length=64, unique=True, default=genToken, db_index=True
    )

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        # Si el vendedor no está definido, se asigna el creador del catálogo
        if not self.seller and self.created_by:
            self.seller = self.created_by
        super(CatalogMaster, self).save(*args, **kwargs)
        
    class Meta:
        indexes = [
            models.Index(fields=["company_id", "owner"]),
        ]
        db_table = 'catalog_catalogm'
        verbose_name = 'Catalog'
        verbose_name_plural = 'Catalogs'

    def __str_(self):
        return "Catalog {} / {}".format(self.name, self.token)


# Modelo para detalle de catálogo
class CatalogDetail(Common):
    """Modelo para detalle de catálogo"""
    sku = models.CharField("SKU", max_length=50)
    name = models.CharField("Nombre", max_length=100, blank=True, default='Catalog Item')
    note =  models.TextField("Nota", blank = True)
    price = models.DecimalField("Precio", max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField("Stock", default=0)
    minqty = models.IntegerField("Cantidad Mínima", default=1)
    maxqty = models.IntegerField("Cantidad Máxima", default=1000)
    tags = models.ManyToManyField(Tag, related_name='catalog_details_tag', blank=True)
    category = models.ForeignKey(Category, related_name='catalog_details_category', blank=True, null=True, on_delete=models.SET_NULL)
    catalog =  models.ForeignKey(CatalogMaster, related_name='catalog_details', on_delete=models.CASCADE)
    brand = models.CharField("Marca", max_length=100, blank=True, null=True)
    description = models.TextField("Descripción", blank=True, null=True)

    class Meta:
        db_table = 'catalog_catalogd'
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'

    def __str_(self):
        return "Item {} - {} - {}".format(self.id, self.sku, self.catalog)


# Modelo para imágenes adicionales para cada item del detalle de catálogo
class CatalogDetailImage(Common):
    """Modelo para imágenes adicionales para items del detalle de catálogo"""
    itemdetail = models.ForeignKey(CatalogDetail, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Imagen', upload_to=catalog_path, blank=True)

    class Meta:
        db_table = 'catalog_catalogdimg'
        verbose_name = 'Catalog Detail Images'
        verbose_name_plural = 'Catalog Details Images'

    def __str__(self):
        return "Image {} - {}".format(self.id, self.itemdetail.sku)
