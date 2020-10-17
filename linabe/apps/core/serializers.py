from rest_framework import serializers

from .models import Cia, User

class CiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cia
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('__all__')