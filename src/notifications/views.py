from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from core.permissions import IsOwner

from .models import NotificationPreference
from .serializers import NotificationPreferenceSerializer


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for announcements.
    """

    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = NotificationPreferenceSerializer

    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
