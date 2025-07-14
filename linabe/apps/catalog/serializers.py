from rest_framework import serializers
from .models import Category, Tag, CatalogMaster, CatalogDetail, CatalogDetailImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CatalogMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogMaster
        fields = '__all__'

class CatalogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogDetail
        fields = '__all__'

class CatalogDetailImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogDetailImage
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'modified_at', 'created_by', 'modified_by')


class CatalogSerializer(serializers.ModelSerializer):
    """Serializer para el modelo CatalogMaster con items anidados."""
    catalog_details = CatalogDetailSerializer(many=True)

    class Meta:
        model = CatalogMaster
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'modified_at', 'seller')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        catalog_master = CatalogMaster.objects.create(**validated_data)

        for item_data in items_data:
            CatalogDetail.objects.create(catalog=catalog_master, **item_data)

        return catalog_master

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')

        # Update master data
        instance.name = validated_data.get('name', instance.name)
        instance.seller = validated_data.get('seller', instance.seller)
        instance.ttl = validated_data.get('ttl', instance.ttl)
        instance.descrip = validated_data.get('descrip', instance.descrip)
        instance.note = validated_data.get('note', instance.note)
        instance.customer.set(validated_data.get('customer', instance.customer.all()))
        instance.save()

        # Clear existing items and create new ones
        instance.items.all().delete()
        for item_data in items_data:
            CatalogDetail.objects.create(catalog=instance, **item_data)

        return instance
