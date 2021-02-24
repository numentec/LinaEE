from rest_framework import serializers
from .models import BICatalog, BIFavorito


class BICatalogSerializer(serializers.ModelSerializer):
    """Catálogo para LinaBI"""

    class Meta:
        model = BICatalog
        fields = '__all__'

class BIFavoritoSerializer(serializers.ModelSerializer):
    """Favoritos de LinaBI"""

    class Meta:
        model = BIFavorito
        fields = '__all__'
