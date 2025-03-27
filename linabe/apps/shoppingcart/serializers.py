from rest_framework import serializers
from .models import ExtOrderMaster, ExtOrderItem


class ExtOrderItemSerializer(serializers.ModelSerializer):

    # Campo personalizado que no está en el modelo
    image = serializers.SerializerMethodField()

    class Meta:
        model = ExtOrderItem
        fields = ['id', 'sku', 'name', 'quantity', 'price', 'discount_percentage', 'discount', 'tax', 'total', 'image']
        read_only_fields = ('id',)

    def get_image(self, obj):
        # Devuelve el valor del campo sku concatenado con ".JPG"
        return f"{obj.sku}.JPG"


class ExtOrderMasterSerializer(serializers.ModelSerializer):
    items = ExtOrderItemSerializer(many=True)

    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    modified_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = ExtOrderMaster
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'created_by', 'modified_by')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = ExtOrderMaster.objects.create(**validated_data)

        for item_data in items_data:
            ExtOrderItem.objects.create(extorder=order, **item_data)

        return order
    
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')

        # Update master data
        instance.ciaext = validated_data.get('ciaext', instance.ciaext)
        instance.customer_id = validated_data.get('customer_id', instance.customer_id)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.customer_email = validated_data.get('customer_email', instance.customer_email)
        instance.customer_cel = validated_data.get('customer_cel', instance.customer_cel)
        instance.sendto = validated_data.get('sendto', instance.sendto)
        instance.sendcc = validated_data.get('sendcc', instance.sendcc)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.saleref = validated_data.get('saleref', instance.saleref)
        instance.link = validated_data.get('link', instance.link)
        instance.perm = validated_data.get('perm', instance.perm)
        instance.source = validated_data.get('source', instance.source)
        instance.discount_percentage = validated_data.get('discount_percentage', instance.discount_percentage)
        instance.subtotal = validated_data.get('subtotal', instance.subtotal)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.tax = validated_data.get('tax', instance.tax)
        instance.total = validated_data.get('total', instance.total)
        instance.save()

        # Clear existing items and create new ones
        instance.items.all().delete()
        for item_data in items_data:
            ExtOrderItem.objects.create(extorder=instance, **item_data)

        return instance


class ExtOrderMasterOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExtOrderMaster
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'created_by')
