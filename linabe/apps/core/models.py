from django.db import models, transaction, OperationalError

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

# Imports for token signal on User model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from . import managers

# Modelo para información de compañías
class Cia(models.Model):

    DEFAULT_PK = 1

    codigo = models.CharField('Código', max_length=5, unique=True, help_text = 'Código único interno para la compañía')
    nombre = models.CharField('Nombre', max_length=60, help_text = 'Nombre completo de la compañía')
    nombre_corto = models.CharField('Nombre Corto', max_length=30, blank=True, help_text = 'Nombre abreviado de la compañía')
    ruc = models.CharField('RUC', max_length=30, blank=True, default= '000000-0-000000', help_text = 'Registro único de contribuyente')
    dv = models.CharField('DV', max_length=3, blank=True, default='000', help_text = 'Dígito verificador')
    padre = models.ForeignKey('Cia', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Cia Padre')
    direccion = models.TextField('Dirección', blank=True)
    email = models.EmailField('E-mail', max_length=100, blank=True)
    website = models.URLField('URL', blank=True)
    tel1 = models.CharField('Tel1', max_length=15, blank=True)
    tel2 = models.CharField('Tel2', max_length=15, blank=True)
    fax = models.CharField('Fax', max_length=15, blank=True)
    otros_tels = models.CharField('Otros Tels', max_length=60, blank=True)
    observacion = models.TextField('Observación', blank=True)
    logopath = models.ImageField('Logo', upload_to='images', blank=True, default='images/no_image.png')
    logo_url    = models.TextField(blank=True, null=True)
    soporte_idcli = models.CharField(max_length=10, blank=True, default='numencli')
    country     = models.CharField(max_length=64, blank=True, null=True)
    is_active   = models.BooleanField('Activo', default=True)
    created_at  = models.DateTimeField('Fecha de creación', auto_now_add=True, editable=False)
    modified_at = models.DateTimeField('Fecha de modificación', auto_now=True, editable=False)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        db_table = 'core_cia'
        verbose_name = 'Compañía'
        verbose_name_plural = 'Compañías'


# Usuarios de LinaEE
class User(AbstractUser):

    LOCALE_CHOICES = [
        ('es_PA', 'Español PA'),
        ('en_US', 'Inglés EEUU'),
    ]

    dni = models.CharField('DNI', max_length=30, blank=True, help_text='Documento Nacional de Identidad')
    direccion = models.CharField('Dirección', max_length=60, blank=True)
    tel1 = models.CharField('Tel1', max_length=15, blank=True)
    tel2 = models.CharField('Tel2', max_length=15, blank=True)
    tel3 = models.CharField('Tel3', max_length=15, blank=True)
    nombre_corto = models.CharField('Nombre Corto', max_length=10, blank=True, 
                                        help_text='(Display name) Dejar en blanco para autogenerar')
    localization = models.CharField('Localización', max_length=5, choices=LOCALE_CHOICES, default='es_PA')
    foto = models.ImageField('Foto', upload_to='images/profiles', blank=True, default='images/profiles/no_image_user.png')
    birth_date = models.DateField('Fecha de Nacimiento', blank=True, null=True)
    cia = models.ForeignKey(Cia, blank=True, null=True, verbose_name='Cia Predeterminada',
                                 on_delete=models.SET_NULL, related_name='users_x_cia')
    bio = RichTextField(null=True, blank=True)
    city = models.CharField(blank=True, max_length=100, default='')
    country = models.CharField(blank=True, max_length=100, default='')

    modified_at = models.DateTimeField('Fecha de modificación', auto_now=True, editable=False)

    def __str__(self):
        return '{}'.format(self.get_username())

    def save(self, *args, **kwargs):

        if not self.nombre_corto:
            if self.get_short_name():
                self.nombre_corto = self.get_short_name()
            else:
                self.nombre_corto = self.get_username()

        super(User, self).save(*args, **kwargs)

    class Meta:

        permissions =   (
                            ("view_module_crm", "Access to CRM Module"),
                            ("view_module_sales", "Access to Sales Module"),
                            ("view_module_purchase", "Access to Purchase Module"),
                            ("view_module_inv", "Access to Inventory Module"),
                            ("view_module_hr", "Access to HR Module"),
                            ("view_module_accounting", "Access to Accounting Module"),
                            ("view_module_logistics", "Access to Logistics Module"),
                            ("view_module_linabi", "Access to BI Module"),
                            ("view_module_sys", "Access to System Module")     
                        )

LinaUserModel = get_user_model()

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
@receiver(post_save, sender=LinaUserModel)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Clase abstracta para usarla como base
class Common(models.Model):
    is_active   = models.BooleanField('Activo', default=True)
    created_at  = models.DateTimeField('Fecha de creación', auto_now_add=True, editable=False)
    modified_at = models.DateTimeField('Fecha de modificación', auto_now=True, editable=False)
    created_by  = models.ForeignKey(LinaUserModel, null=True, db_index=True, editable=False, 
                    verbose_name='Creado por', on_delete=models.SET_NULL,
                    related_name='%(class)s_created')
    modified_by = models.ForeignKey(LinaUserModel, null=True, db_index=True, editable=False, 
                    verbose_name='Modificado por', on_delete=models.SET_NULL,
                    related_name='%(class)s_modified')

    class Meta:
        abstract = True


# Datos base para la identidad de una persona Natural o Jurídica
class Identidad(models.Model):

    PERSON_CHOICES = [
        ('N', 'Natural'),
        ('J', 'Jurídica'),
    ]

    codigo = models.CharField('Código', max_length=10, unique=True, help_text='Código Interno')
    nombre = models.CharField('Nombre', max_length=100, blank=True, db_index=True, default='')
    ruc = models.CharField('RUC', max_length=30, blank=True, default='')
    dv = models.CharField('DV', max_length=2, blank=True, default='')
    direccion = models.TextField('Dirección', max_length=100, blank=True, default='')
    tel1 = models.CharField('Teléfono1', max_length=15, blank=True, default='')
    tel2 = models.CharField('Teléfono2',max_length=15, blank=True, default='')
    tel3 = models.CharField('Teléfono3',max_length=15, blank=True, default='')
    email = models.EmailField('Email', max_length=100, blank=True, default='')
    tipo = models.CharField('Tipo', max_length=1, choices=PERSON_CHOICES, default='N')

    class Meta:
        abstract = True


# Generador de secuencias
class GenSequence(models.Model):
    nombre = models.CharField('Nombre', max_length=15, unique=True, help_text='Nombre de la secuencia')
    conteo = models.IntegerField('Conteo', default=0, help_text='Cuenta de la secuencia')
    obs = models.CharField('Observación', max_length=25, blank=True, null=True)

    @classmethod
    def genSec(cls, sec_name, init_val): 
        with transaction.atomic():

            vconteo = 0

            obj, vcreated = cls.objects.select_for_update().get_or_create(nombre=sec_name)

            if vcreated :
                vconteo = init_val
            else:
                vconteo = obj.conteo + 1

            obj.conteo = vconteo
            obj.save()

        return vconteo

    def __str__(self):
        return '{} {}'.format(self.nombre, self.conteo)
    class Meta:
        db_table = 'core_gensequence'
        verbose_name = 'Secuencia'
        verbose_name_plural = 'Secuencias'


# Identificador de hasta tres caracteres para uso discrecional del usuario
# Ej.: A, B, C, CR1, ... X, Y, Z, P25, Z01, etc.
class TipoGenerico(Common):
    
    idgenerico = models.CharField('ID Genérico', max_length=3, unique=True, help_text='Identificador para propósitos generales')
    descripcion = models.CharField('Descripción', max_length=15, blank=True, default='')

    def __str__(self):
        return '{}'.format(self.idgenerico)
    class Meta:
        db_table = 'core_tipo_generico'
        verbose_name = 'Tipo Generico'
        verbose_name_plural = 'Tipos Genericos'
        ordering = ['idgenerico']


# Modelo del sistema. Módulos
class Modulo(Common):
    nombre = models.CharField('Nombre', max_length=25, unique=True)
    descrip = models.CharField('Descripción', max_length=50, blank=True)
    tipo = models.PositiveIntegerField('Tipo', default=0)

    def __str__(self):
        return 'Módulo {}'.format(self.nombre)

    class Meta:
        db_table = 'core_modulos'
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'


# Modelo del sistema. Vistas o formularios por módulo
class Vista(Common):
    nombre = models.CharField('Nombre', max_length=25, unique=True)
    descrip = models.CharField('Descripción', max_length=50, blank=True)
    link = models.CharField('Enlace Interno', max_length=100, default='/')
    tipo = models.PositiveIntegerField('Tipo', default=0)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, verbose_name='Módulo', related_name='vistas_x_modulo')

    def __str__(self):
        return 'Vista {}'.format(self.nombre)

    class Meta:
        db_table = 'core_vistas'
        verbose_name = 'Vista'
        verbose_name_plural = 'Vistas'


# Modelo del sistema. Configuración de la vista o formulario
class VistaConfig(Common):
    vista = models.ForeignKey(Vista, on_delete=models.CASCADE, verbose_name='Vista', related_name='configs_x_vista')
    configkey = models.CharField(max_length=20)
    configval1 = models.CharField(max_length=20, blank=True)
    configval2 = models.CharField(max_length=20, blank=True)
    configval3 = models.CharField(max_length=20, blank=True)
    configval4 = models.CharField(max_length=20, blank=True)
    configval5 = models.CharField(max_length=20, blank=True)
    configval6 = models.CharField(max_length=20, blank=True)
    configval7 = models.CharField(max_length=20, blank=True)
    configval8 = models.CharField(max_length=20, blank=True)
    configval9 = models.CharField(max_length=20, blank=True)
    tipo = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return 'Config vista {}'.format(self.vista.nombre)

    class Meta:
        db_table = 'core_vistaconfig'
        verbose_name = 'Configuración por Vista'
        verbose_name_plural = 'Configuraciones por Vista'


# Modelo del sistema. Configuración de la vista o formulario por usuario
class VistaConfigUser(Common):
    user = models.ForeignKey(LinaUserModel, on_delete=models.CASCADE, verbose_name='Usuario', related_name='vistaconfigs_x_user')
    vista = models.ForeignKey(Vista, on_delete=models.CASCADE, verbose_name='Vista', related_name='confuser_x_vista')
    configkey = models.CharField(max_length=20)
    configval1 = models.CharField(max_length=20, blank=True)
    configval2 = models.CharField(max_length=20, blank=True)
    configval3 = models.CharField(max_length=20, blank=True)
    configval4 = models.CharField(max_length=20, blank=True)
    configval5 = models.CharField(max_length=20, blank=True)
    configval6 = models.CharField(max_length=20, blank=True)
    configval7 = models.CharField(max_length=20, blank=True)
    configval8 = models.CharField(max_length=20, blank=True)
    configval9 = models.CharField(max_length=20, blank=True)
    tipo = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return 'Config vista {} usuario {}'.format(self.vista.nombre, self.user.username)

    class Meta:
        db_table = 'core_vistaconfiguser'
        verbose_name = 'Configuración por Vista y Usuario'
        verbose_name_plural = 'Configuraciones por Vista y Usuario'


# Modelo para manejo de Clientes, Proveedores, Bancos, Socios y similares
class StakeHolder(Common, Identidad):

    LOCALE_CHOICES = [
        ('es_PA', 'Español PA'),
        ('en_US', 'Inglés EEUU'),
    ]

    DIASCR_CHOICES = [
        (15, '15 días'),
        (30, '30 días'),
        (45, '45 días'),
        (60, '60 días'),
        (90, '90 días'),
        (120, '120 días'),
    ]

    DEFAULT_PK = 1

    cred = models.BooleanField('Crédito', blank=True, default=False, help_text='Indica si es de tipo crédito')
    exonerado = models.BooleanField('Exonerado', blank=True, default=False, help_text='Exonerado de impuestos')
    ordencompra = models.BooleanField('Orden Compra', blank=True, default=False, help_text='Requerir orden de compra')
    diascr = models.DecimalField('Días CR', max_digits=3, decimal_places=0, choices=DIASCR_CHOICES, default=30, help_text='Días de Crédito')
    maxcr = models.DecimalField('Max CR', max_digits=12, decimal_places=2, blank=True, default=0.00, help_text='Máximo crédito otorgado')
    contacto = models.CharField('Contacto', max_length=50, blank=True, null=True)
    idgenerico = models.ForeignKey(TipoGenerico, on_delete=models.CASCADE, verbose_name='ID Genérico', help_text='Identificador para propósitos generales')
    descauto = models.DecimalField('Descuento Automático', max_digits=6, decimal_places=3, blank=True, default=0.000, \
        help_text='Aplicar descuento en porciento de forma automática')
    retencion = models.DecimalField(max_digits=6, decimal_places=3, blank=True, default=0.000, \
        help_text='Porcentaje a retener')
    is_cli = models.BooleanField('Cliente', blank=True, default=False, help_text='Es cliente')
    is_pro = models.BooleanField('Proveedor', blank=True, default=False, help_text='Es proveedor')
    is_ban = models.BooleanField('Banco', blank=True, default=False, help_text='Es banco')
    is_soc = models.BooleanField('Socio', blank=True, default=False, help_text='Es socio')
    foto = models.ImageField('Foto', upload_to='images/stakeholders', blank=True, default='images/profiles/no_image_user.png')
    birth_date = models.DateField('Fecha de Nacimiento', blank=True, null=True)
    locale = models.CharField('Localización', max_length=5, choices=LOCALE_CHOICES, default='es_PA')
    website = models.URLField('URL', blank=True, null=True)

    objects =  models.Manager()
    stakeholders =  managers.StakeHolder()

    def __str__(self):
        return '{} ({})'.format(self.nombre, self.codigo)

    class Meta:
        db_table = 'core_stakeholders'
        verbose_name = 'Stakeholder'
        verbose_name_plural = 'Stakeholders'

        permissions =   (
                            ("view_cliente", "View customers details or list"),
                            ("create_cliente", "Create customer"),
                            ("update_cliente", "Update customer"),
                            ("change_cliente_cr", "Edit customer credit"),
                            ("view_proveedor", "View supplier details or list"),
                            ("create_proveedor", "Create supplier"),
                            ("update_proveedor", "Update supplier"),
                            ("change_proveedor_cr", "Edit supplier credit"),
                            ("view_banco", "View bank details or list"),
                            ("create_banco", "Create bank"),
                            ("update_banco", "Update bank"),
                            ("view_socio", "View partner details or list"),
                            ("create_socio", "Create partner"),
                            ("update_socio", "Update partner"),
                        )
