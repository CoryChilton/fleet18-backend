from .models import Racer, User
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

class RacerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for racers.
    """
    queryset = Racer.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RacerSerializer
