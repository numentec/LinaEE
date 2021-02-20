from django.db import models
from .attributs import attrs_catalog

# Create your models here.
class TransientModel(models.Model):
    """Inherit from this class to use django constructors and serialization but no database management"""
    def save(*args, **kwargs):
        pass  # avoid exceptions if called

    class Meta:
        abstract = True  # no table for this class
        managed = False  # no database management

BICatalog = type("BICatalog", (TransientModel,), attrs_catalog)
