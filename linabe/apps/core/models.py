from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

# Imports for token signal on User model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Modelo para información de compañías
class Cia(models.Model):

    DEFAULT_PK = 1

    codigo = models.CharField('Código', max_length=5, unique=True, help_text = 'Código único interno para la compañía')
    nombre = models.CharField('Nombre', max_length=60, help_text = 'Nombre completo de la compañía')
    nombre_corto = models.CharField('Nombre Corto', max_length=30, blank=True, help_text = 'Nombre abreviado de la compañía')
    ruc = models.CharField('RUC', max_length=30, blank=True, default= '000000-0-000000', help_text = 'Registro único de contribuyente')
    dv = models.CharField('DV', max_length=3, blank=True, default='000', help_text = 'Dígito verificador')
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
        db_table = 'lina_core_cia'
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

        super(User, self).save(*args, **kwargs)

        if not self.nombre_corto:
            if self.get_short_name():
                self.nombre_corto = self.get_short_name()
            else:
                self.nombre_corto = self.get_username()

    class Meta:

        permissions =   (
                            ("view_crm_module", "Access to CRM Module"),
                            ("view_sales_module", "Access to Sales Module"),
                            ("view_purchase_module", "Access to Purchase Module"),
                            ("view_inv_module", "Access to Inventory Module"),
                            ("view_hr_module", "Access to HR Module"),
                            ("view_accounting_module", "Access to Accounting Module"),
                            ("view_logistics_module", "Access to Logistics Module"),
                            ("view_linabi_module", "Access to BI Module"),
                            ("view_sys_module", "Access to System Module")   
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
