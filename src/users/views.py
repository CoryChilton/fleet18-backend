from .models import Racer
from rest_framework import viewsets, permissions
from .serializers import RacerSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class RacerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for racers.
    """
    queryset = Racer.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RacerSerializer
