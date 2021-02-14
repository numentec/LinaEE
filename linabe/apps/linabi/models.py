from django.db import models

# Create your models here.
class TransientModel(models.Model):
    """Inherit from this class to use django constructors and serialization but no database management"""
    def save(*args, **kwargs):
        pass  # avoid exceptions if called

    class Meta:
        abstract = True  # no table for this class
        managed = False  # no database management

class BICatalog(TransientModel):
    """This is not persisted. No table linabi_catalog"""
    #do more things here
    sku = models.CharField('SKU', max_length=30, blank=True, null=True)
    distro = models.CharField('Distro', max_length=20, blank=True, null=True)
    
    class Meta:
        ordering = ['sku']
