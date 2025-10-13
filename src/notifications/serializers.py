from .models import NotificationPreference
from rest_framework import serializers
from django.utils import timezone

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = '__all__'