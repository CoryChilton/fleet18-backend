from .models import Racer
from rest_framework import serializers
from django.utils import timezone

class RacerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Racer
        fields = '__all__'