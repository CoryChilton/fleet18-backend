from rest_framework import serializers

from .models import EventPhoto


class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPhoto
        fields = "__all__"
        read_only_fields = ["user"]
