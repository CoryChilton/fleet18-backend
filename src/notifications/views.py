from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from .models import NotificationPreference
from .serializers import NotificationPreferenceSerializer


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for announcements.
    """

    queryset = NotificationPreference.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = NotificationPreferenceSerializer
