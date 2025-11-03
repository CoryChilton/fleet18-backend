from django.utils import timezone
from rest_framework import serializers

from .models import Event, Race, Result


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    def validate_event_time(self, value):
        """ "
        Check that the expiration timestamp is greater than current time
        """
        if value < timezone.now():
            raise serializers.ValidationError("Event time cannot be in the past.")
        return value


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"
