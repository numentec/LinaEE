from rest_framework import serializers
from .models import BICatalog, BIFavorito, BIQuery, BIXLSXTemplate, BIXLSXTemplateCol, BICustomCatalogMaster, BICustomCatalogDetail
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


class BICustomCatalogDetailSerializer(serializers.ModelSerializer):
    """Modelo para detalle de catálogo personalizado"""
    # created_by = serializers.PrimaryKeyRelatedField(queryset=LinaUserModel.objects.all(), required=False)
    # updated_by = serializers.PrimaryKeyRelatedField(queryset=LinaUserModel.objects.all(), required=False)

    class Meta:
        model = BICustomCatalogDetail
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'modified_by')
        extra_kwargs = {
            'created_by': {'required': False},
            'modified_by': {'required': False}
        }

class BICustomCatalogMasterSerializer(serializers.ModelSerializer):
    """Modelo para maestro de catálogo personalizado"""
    # created_by = serializers.PrimaryKeyRelatedField(queryset=LinaUserModel.objects.all(), required=False)
    # updated_by = serializers.PrimaryKeyRelatedField(queryset=LinaUserModel.objects.all(), required=False)
    details = BICustomCatalogDetailSerializer(many=True)

    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    modified_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = BICustomCatalogMaster
        fields = '__all__'
        read_only_fields = ('id', 'token', 'created_at', 'created_by', 'modified_by')
        extra_kwargs = {
            'created_by': {'required': False},
            'modified_by': {'required': False}
        }

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        catalog = BICustomCatalogMaster.objects.create(**validated_data)

        for detail_data in details_data:
            BICustomCatalogDetail.objects.create(customcatalog=catalog, **detail_data)

        return catalog
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details')

        # Update master data
        instance.name = validated_data.get('name', instance.name)
        instance.descrip = validated_data.get('descrip', instance.descrip)
        instance.note = validated_data.get('note', instance.note)
        instance.token = validated_data.get('token', instance.token)
        instance.ttl = validated_data.get('ttl', instance.ttl)
        instance.stakeholder = validated_data.get('stakeholder', instance.stakeholder)
        instance.save()

        # Clear existing details and create new ones
        instance.details.all().delete()
        for detail_data in details_data:
            BICustomCatalogDetail.objects.create(customcatalog=instance, **detail_data)

        return instance
    
class BICustomCatalogMasterOnlySerializer(serializers.ModelSerializer):
    """Modelo para maestro de catálogo personalizado"""
    # created_by = serializers.PrimaryKeyRelatedField(queryset=LinaUserModel.objects.all(), required=False)
    # updated_by = serializers.PrimaryKeyRelatedField(queryset=LinaUserModel.objects.all(), required=False)

    class Meta:
        model = BICustomCatalogMaster
        fields = '__all__'
        read_only_fields = ('id', 'token', 'created_at', 'created_by', 'modified_by')
        extra_kwargs = {
            'created_by': {'required': False},
            'modified_by': {'required': False}
        }