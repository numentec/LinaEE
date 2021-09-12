from rest_framework import serializers
from .models import WMSQuery
from django.contrib.auth import get_user_model

LinaUserModel = get_user_model()

class WMSQuerySerializer(serializers.ModelSerializer):
    """WMSQuery de WMS"""

    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.created_by.username
        
    class Meta:
        model = WMSQuery
        fields = '__all__'
        read_only_fields = ('id', 'username')
