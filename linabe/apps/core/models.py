from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

# Clase abstracta para usarla de base
class Common(models.Model):
    is_active   = models.BooleanField('Activo', default=True)
    created_at  = models.DateTimeField('Fecha de creación', auto_now_add=True, editable=False)
    modified_at = models.DateTimeField('Fecha de modificación', auto_now=True, editable=False)
    created_by  = models.ForeignKey(User, null=True, db_index=True, editable=False, 
                    verbose_name='Creado por', on_delete=models.SET_NULL,
                    related_name='%(class)s_created')
    modified_by = models.ForeignKey(User, null=True, db_index=True, editable=False, 
                    verbose_name='Modificado por', on_delete=models.SET_NULL,
                    related_name='%(class)s_modified')

    class Meta:
        abstract = True

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
    soporte_idcli = models.CharField(max_length=10, blank=True, default='numencli')
    country     = models.CharField(max_length=64, blank=True, null=True)
    logo_url    = models.TextField(blank=True, null=True)

    def __str__(self):
        #return '{} {} {}'.format(self.id, self.codigo, self.nombre)
        return '{}'.format(self.nombre)

    class Meta:
        db_table = 'lina_core_cia'
        verbose_name = 'Compañía'
        verbose_name_plural = 'Compañías'


# Perfil de usuarios de Lina
class Perfil(Common):

    LOCALE_CHOICES = [
        ('es_PA', 'Español PA'),
        ('en_US', 'Inglés EEUU'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
                                 on_delete=models.SET_NULL, related_name='perfiles_x_cia')

    def __str__(self):
        #return '{} {} {} {}'.format(self.id, self.user.get_username(), self.user.get_full_name(), self.user.last_login)
        return '{}'.format(self.user.get_username())

    def save(self, *args, **kwargs):

        super(Perfil, self).save(*args, **kwargs)

        if not self.nombre_corto:
            if self.user.get_short_name():
                self.nombre_corto = self.user.get_short_name()
            else:
                self.nombre_corto = self.user.get_username()

    class Meta:
        db_table = 'lina_core_perfil'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

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


@receiver(post_save, sender=User)
def create_user_perfil(sender, instance, created, **kwargs):
   if created:
       Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_perfil(sender, instance, **kwargs):
   instance.perfil.save()
