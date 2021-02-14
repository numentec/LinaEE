from rest_framework import serializers
from .models import BICatalog


class BICatalogSerializer(serializers.ModelSerializer):
    """Catálogo para LinaBI"""

    class Meta:
        model = BICatalog
        fields = '__all__'
