from .models import Event, Result
from rest_framework import serializers
from django.utils import timezone

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate_event_time(self, value):
        """"
        Check that the expiration timestamp is greater than current time
        """
        if value < timezone.now():
            raise serializers.ValidationError("Event time cannot be in the past.")
        return value
    
    def validate_entry_fee(self, value):
        """
        Check the entry fee is non-negative
        """
        if value < 0:
            raise serializers.ValidationError("Entry fee must be non-negative.")
        return value

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
    
    