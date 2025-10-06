from .models import Event
from rest_framework import viewsets, permissions
from .serializers import EventSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for announcements.
    """
    queryset = Event.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EventSerializer
