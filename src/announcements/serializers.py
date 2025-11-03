from django.utils import timezone
from rest_framework import serializers

from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"

    def validate_expiration_timestamp(self, value):
        """ "
        Check that the expiration timestamp is greater than current time
        """
        if value < timezone.now():
            raise serializers.ValidationError("Expiration time cannot be in the past.")
        return value
