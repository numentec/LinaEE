from rest_framework import serializers

from .models import Cia

class CiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cia
        fields = ('__all__')