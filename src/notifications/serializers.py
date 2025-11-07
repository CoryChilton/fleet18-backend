from rest_framework import serializers

from .models import NotificationPreference


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, attrs):
        """
        Check that the user doesn't already have a preference for this
        notification type.
        """
        user = self.context["request"].user
        notification_type = attrs.get("notification_type")

        # Check if updating existing instance or creating new one
        if self.instance:
            # Updating: check if another preference with same type exists
            # (excluding current instance)
            existing = NotificationPreference.objects.filter(
                user=user, notification_type=notification_type
            ).exclude(pk=self.instance.pk)
        else:
            # Creating: check if preference already exists
            existing = NotificationPreference.objects.filter(
                user=user, notification_type=notification_type
            )

        if existing.exists():
            raise serializers.ValidationError(
                {
                    "notification_type": "A preference for this notification type already exists."  # noqa E501
                }
            )

        return attrs
