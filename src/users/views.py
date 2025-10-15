from .models import Racer, User
from notifications.models import NotificationPreference
from notifications.serializers import NotificationPreferenceSerializer
from rest_framework import viewsets, permissions
from .serializers import RacerSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    """
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'], url_path='notification-preferences')
    def notification_preferences(self, request, pk=None):
        user = self.get_object()
        prefs = NotificationPreference.objects.filter(user=user)
        serializer = NotificationPreferenceSerializer(prefs, many=True)
        return Response(serializer.data)

class RacerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for racers.
    """
    queryset = Racer.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RacerSerializer
