from .models import NotificationPreference
from rest_framework import viewsets, permissions
from .serializers import NotificationPreferenceSerializer
from rest_framework.decorators import action

class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for announcements.
    """
    queryset = NotificationPreference.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = NotificationPreferenceSerializer
