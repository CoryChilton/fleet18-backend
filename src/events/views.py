from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import IsAdminOrReadOnly

from .models import Event, Race, Result
from .serializers import EventSerializer, RaceSerializer, ResultSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for events.
    """

    queryset = Event.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = EventSerializer


class RaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for races.
    """

    queryset = Race.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = RaceSerializer


class ResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint for results.
    """

    queryset = Result.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ResultSerializer
    filterset_fields = ("race__event", "race", "racer")
