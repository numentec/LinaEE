from rest_framework import serializers
from .models import BICatalog, BIFavorito, BIQuery, BIXLSXTemplate, BIXLSXTemplateCol
from django.contrib.auth import get_user_model

LinaUserModel = get_user_model()

class BICatalogSerializer(serializers.ModelSerializer):
    """Catálogo para LinaBI"""

    class Meta:
        model = BICatalog
        fields = '__all__'

class BIQuerySerializer(serializers.ModelSerializer):
    """BIQuery de LinaBI"""

    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.created_by.username

    class Meta:
        model = BIQuery
        fields = '__all__'
        read_only_fields = ('id', 'username')

class BIFavoritoSerializer(serializers.ModelSerializer):
    """Favoritos de LinaBI"""

    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.owner.username
        
    class Meta:
        model = BIQuery
        fields = '__all__'
        read_only_fields = ('id', 'username')

class BIXLSXTemplateColSerializer(serializers.ModelSerializer):
    """Columnas de Plantillas XLSX en LinaBI"""

    class Meta:
        model = BIXLSXTemplateCol
        fields = ('id', 'name', 'ordinal', 'posicion')

class BIXLSXTemplateSerializer(serializers.ModelSerializer):
    """Plantillas XLSX en LinaBI"""

    cols_x_plantilla = BIXLSXTemplateColSerializer(read_only = True, many = True)

    class Meta:
        model = BIXLSXTemplate
        fields = '__all__'
