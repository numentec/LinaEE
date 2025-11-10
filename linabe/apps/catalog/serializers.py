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


class CatalogDetailCustomerSerializer(serializers.ModelSerializer):
    """Serializer para items del catálogo con nombres de campos personalizados."""
    item_id = serializers.IntegerField(source='id')
    id = serializers.CharField(source='sku')
    instock = serializers.IntegerField(source='stock')
    image = serializers.SerializerMethodField()

    # def get_image(self, obj):
    #     """Obtiene la URL de la imagen principal del item del catálogo."""
    #     if obj.images.exists():
    #         request = self.context.get('request')
    #         image_url = obj.images.first().image.url
    #         return request.build_absolute_uri(image_url) if request else image_url
    #     return None
    
    def get_image(self, obj):
        """Genera imagen .jpg a partir del sku del item del catálogo."""
        # Lógica para generar la imagen basada en el SKU
        return f"{obj.sku}.jpg"


    class Meta:
        model = CatalogDetail
        fields = ('item_id', 'id', 'name', 'description', 'price', 'instock', 
                 'image', 'brand', 'minqty', 'maxqty')


class CatalogCustomerSerializer(serializers.ModelSerializer):
    """Serializer personalizado para el catálogo con items anidados. Para vista de clientes"""

    items = CatalogDetailCustomerSerializer(source='catalog_details', many=True)
    
    class Meta:
        model = CatalogMaster
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'modified_at', 'seller')


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
