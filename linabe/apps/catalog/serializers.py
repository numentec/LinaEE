from rest_framework import serializers
from .models import Category, Tag, CatalogMaster, CatalogDetail, CatalogDetailImage
from ..core.models import Cia


class CiaSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple para mostrar información básica de Cia"""
    class Meta:
        model = Cia
        fields = ('id', 'codigo', 'nombre', 'nombre_corto')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryWithCompaniesSerializer(serializers.ModelSerializer):
    """Serializer para Category que incluye las compañías disponibles"""
    available_companies = CiaSimpleSerializer(source='available_for_companies', many=True, read_only=True)
    available_companies_count = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    children_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'parent_name', 'description', 'ext_related_id', 
                 'image', 'available_companies', 'available_companies_count', 'children_count',
                 'created_at', 'modified_at', 'is_active')
    
    def get_available_companies_count(self, obj):
        """Retorna el número de compañías para las que está disponible"""
        return obj.available_for_companies.count()
    
    def get_children_count(self, obj):
        """Retorna el número de subcategorías"""
        return obj.children.count()


class CategoryHierarchySerializer(serializers.ModelSerializer):
    """Serializer para mostrar categorías en jerarquía (padre e hijos)"""
    available_for_company = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    brands = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'ext_related_id', 'image', 
                 'available_for_company', 'children', 'brands', 'created_at', 'is_active')
    
    def get_available_for_company(self, obj):
        """Verifica si está disponible para la compañía del contexto"""
        company_id = self.context.get('company_id')
        if not company_id:
            return True
        try:
            company = Cia.objects.get(id=company_id)
            return obj.is_available_for_company(company)
        except Cia.DoesNotExist:
            return False
    
    def get_children(self, obj):
        """Retorna las subcategorías si es necesario"""
        include_children = self.context.get('include_children', False)
        if include_children:
            children = obj.children.filter(is_active=True)
            return CategoryHierarchySerializer(children, many=True, context=self.context).data
        return []
    
    def get_brands(self, obj):
        """Retorna las marcas asociadas a la categoría"""
        include_brands = self.context.get('include_brands', False)
        if include_brands:
            brands = obj.brands.filter(is_active=True)
            return TagSerializer(brands, many=True).data
        return []

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

# Previously implemented serializer for CatalogMaster with nested items.
# class CatalogSerializer(serializers.ModelSerializer):
#     """Serializer para el modelo CatalogMaster con items anidados."""
#     catalog_details = CatalogDetailSerializer(many=True)

#     class Meta:
#         model = CatalogMaster
#         fields = '__all__'
#         read_only_fields = ('id', 'created_at', 'modified_at', 'seller')

#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
#         catalog_master = CatalogMaster.objects.create(**validated_data)

#         for item_data in items_data:
#             CatalogDetail.objects.create(catalog=catalog_master, **item_data)

#         return catalog_master

#     def update(self, instance, validated_data):
#         items_data = validated_data.pop('items')

#         # Update master data
#         instance.name = validated_data.get('name', instance.name)
#         instance.seller = validated_data.get('seller', instance.seller)
#         instance.ttl = validated_data.get('ttl', instance.ttl)
#         instance.descrip = validated_data.get('descrip', instance.descrip)
#         instance.note = validated_data.get('note', instance.note)
#         instance.customer.set(validated_data.get('customer', instance.customer.all()))
#         instance.save()

#         # Clear existing items and create new ones
#         instance.items.all().delete()
#         for item_data in items_data:
#             CatalogDetail.objects.create(catalog=instance, **item_data)

#         return instance


# Serializer para el modelo Catalog (AI generado)
class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogMaster
        fields = (
            "id",
            "company_id",
            "name",
            "template",
            "orientation",
            "settings",
            "theme",
            "pages",
            "share_token",
            "updated_at",
        )
        read_only_fields = ("id", "share_token", "updated_at")

# Serializer público para el modelo Catalog (AI generado)
class PublicCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogMaster
        fields = (
            "name",
            "template",
            "orientation",
            "settings",
            "theme",
            "pages",
        )
