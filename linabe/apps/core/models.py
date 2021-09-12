import os
from django.db import models, transaction, OperationalError

from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

# Imports for token signal on User model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from . import managers

def img_profile_path(instance, filename):
    """Guarda foto de perfil con nombre de usuario"""
    ext = filename.split('.')[-1]
    imgname = getattr(instance, 'username')
    filename = f'{imgname}.{ext}'

    return os.path.join('images/profiles/', filename)

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
    foto = models.ImageField('Foto', upload_to=img_profile_path, blank=True, null=True, default='images/profiles/no_image_user.png')
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
        permissions =   [("ext_acc", "Allow external access")]
    


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


# Modelo del sistema. Módulos
class Modulo(models.Model):
    nombre = models.CharField('Nombre', max_length=25, unique=True)
    descrip = models.CharField('Descripción', max_length=50, blank=True)
    tipo = models.PositiveIntegerField('Tipo', default=0)
    is_active = models.BooleanField('Activo', default=False)

    def __str__(self):
        return 'Módulo {}'.format(self.nombre)

    class Meta:
        permissions =   (
                            ("acc_crm", "Access to CRM Module"),
                            ("acc_sales", "Access to Sales Module"),
                            ("acc_purchase", "Access to Purchase Module"),
                            ("acc_inv", "Access to Inventory Module"),
                            ("acc_hr", "Access to HR Module"),
                            ("acc_accounting", "Access to Accounting Module"),
                            ("acc_logistics", "Access to Logistics Module"),
                            ("acc_linabi", "Access to BI Module"),
                            ("acc_config", "Access to Configuration Module"),
                            ("acc_wms", "Access to WMS Module"),
                        )
        db_table = 'core_modulos'
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'


# Modelo del sistema. Vistas o formularios por módulo
class Vista(Common):
    nombre = models.CharField('Nombre', max_length=25, unique=True)
    descrip = models.CharField('Descripción', max_length=50, blank=True)
    link = models.CharField('Enlace Interno', max_length=100, default='/')
    tipo = models.PositiveIntegerField('Tipo', default=0)
    checkelperms = models.BooleanField('Evaluar Permisos', default=True, help_text='Evaluar permisos para elementos de la vista')
    disponible = models.BooleanField('Disponible', default=True)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, verbose_name='Módulo', related_name='vistas_x_modulo')

    def __str__(self):
        return 'Vista {}'.format(self.nombre)

    class Meta:
        permissions =   (
                            ("acc_linabi_catalog", "Access to LinaBI Catalog view"),
                            ("acc_linabi_saledocs_master", "Access to LinaBI Sale Docs Master view"),
                            ("acc_linabi_saledocs_datail", "Access to LinaBI Sale Docs Detail view"),
                            ("acc_linabi_sales_detail", "Access to LinaBI  Sales Detail view"),
                            ("acc_linabi_reports", "Access to LinaBI  Reports view"),
                            ("acc_linabi_storagexloc", "Access to storage by location"),
                            ("acc_wms_relocate_tool", "Access to relocate tool"),
                        )
        db_table = 'core_vistas'
        verbose_name = 'Vista'
        verbose_name_plural = 'Vistas'


# Modelo del sistema. Configuración de la vista o formulario
class VistaConfig(Common):
    vista = models.ForeignKey(Vista, on_delete=models.CASCADE, verbose_name='Vista', related_name='configs_x_vista')
    configkey = models.CharField(max_length=20)
    ordinal = models.IntegerField('Ordinal', default=0, help_text='Para ordenar las llaves de configuración')
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
        return '{} - {} - {} - {}'.format(self.id, self.vista.nombre, self.configkey, self.configval2)

    class Meta:
        ordering = ['vista', 'ordinal']
        db_table = 'core_vistaconfig'
        verbose_name = 'Configuración por Vista'
        verbose_name_plural = 'Configuraciones por Vista'


# Modelo del sistema. Acceso por grupo a clave de configuración de la vista
class VistaConfigAcc(models.Model):
    vistaconf = models.ForeignKey(VistaConfig, on_delete=models.CASCADE, verbose_name='Vistaconf', \
         related_name='acc_x_vistaconf')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Grupo', related_name='acc_x_group')
    acceso = models.BooleanField('Acceso', default=True)

    def __str__(self):
        return 'Acceso a configuración de vista {}'.format(self.vistaconf.configkey)

    class Meta:
        db_table = 'core_vistaconfacc'
        verbose_name = 'Acceso a conf'
        verbose_name_plural = 'Accesos a conf'


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


class DayOfWeek(models.Model):
    name = models.CharField('Día', max_length=10, unique=True)
    abr = models.CharField('Abreviatura', max_length=3, blank=True)

    def __str__(self):
        return 'Día {}'.format(self.name)

    class Meta:
        db_table = 'core_dayofweek'
        verbose_name = 'Dia'
        verbose_name_plural = 'Dias'

def allDays():
    daysList = DayOfWeek.objects.all()
    return daysList

# Modelo del sistema. Direcciones IP sin restricción por origen
class IpWhiteList(Common):
    ip_address = models. GenericIPAddressField('IP', unique=True)
    descrip = models.CharField('Descripción', max_length=25, blank=True, default='')
    reject = models.BooleanField('Rechazar', default=False, help_text="Marcar para denegar acceso desde esta IP")
    hora_ini = models.TimeField('Hora de inicio', default='07:00:00')
    hora_fin = models.TimeField('Hora de fin', default='18:00:00')
    days = models.ManyToManyField(DayOfWeek, default=allDays, verbose_name='Días con acceso')


    def __str__(self):
        return 'Dirección IP {}'.format(self.ip_address)

    class Meta:
        db_table = 'core_ipwhitelist'
        verbose_name = 'IP Whitelist'
        verbose_name_plural = 'IPs Whitelist'


# Modelo del sistema. Consultas SQL por vista
class SQLQuery(Common):

    DB_CHOICES = [
        ('MARIDB', 'MariaDB'),
        ('MYSQL', 'My SQL'),
        ('ORACLE', 'ORACLE DB'),
        ('SQLITE', 'SQLite'),
        ('MSSQL', 'MS SQL Server'),
    ]

    name  = models.CharField('Nombre', max_length=25, default='SQL')
    content = models.TextField('Contenido', blank=True, default='')
    ordinal = models.IntegerField('Ordinal', default=1)
    dbtype = models.CharField('DB Type', max_length=6, choices=DB_CHOICES, default='MARYDB')
    dbuser = models.CharField('DB User', max_length=15, blank=True)
    dbpass = models.CharField('DB Password', max_length=15, blank=True)
    comment = models.CharField('Comentario', max_length=50, blank=True)
    vista = models.ForeignKey(Vista, on_delete=models.CASCADE, verbose_name='Vista', related_name='sqlquery_x_vista')

    def __str__(self):
        return 'SQL Query {}'.format(self.name)

    class Meta:
        db_table = 'core_sqlquery'
        verbose_name = 'Consulta SQl por vista'
        verbose_name_plural = 'Consultas SQl por vista'
        ordering = ['vista', 'ordinal']
