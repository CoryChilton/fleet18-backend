from .models import EventPhoto
from rest_framework import viewsets, permissions
from .serializers import EventPhotoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class EventPhotoViewSet(viewsets.ModelViewSet):
    """
    API endpoint for events.
    """
    queryset = EventPhoto.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EventPhotoSerializer
