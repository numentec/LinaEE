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
    created_by  = models.ForeignKey('Creado por', User,
                    null=True, db_index=True, editable=False,
                    on_delete=models.SET_NULL, related_name="%(class)s_created")
    modified_by = models.ForeignKey('Modificado por', User,
                    null=True, db_index=True, editable=False,
                    on_delete=models.SET_NULL, related_name="%(class)s_modified")

    class Meta:
        abstract = True


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
    nombre_corto = models.CharField('Nombre Corto', max_length=10, blank=True, help_text='(Screen name) Dejar en blanco para autogenerar')
    locale = models.CharField('Localización', max_length=5, choices=LOCALE_CHOICES, default='es_PA')
    foto = models.ImageField('Foto', upload_to='images/profiles', blank=True, default='images/profiles/no_image_user.png')
    birth_date = models.DateField('Fecha de Nacimiento', blank=True, null=True)

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
