from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Race, Result
from .serializers import EventSerializer, RaceSerializer, ResultSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for events.
    """

    queryset = Event.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EventSerializer

    @action(detail=True, methods=["get"], url_path="results")
    def results(self, request, pk=None):
        event = self.get_object()
        results = Result.objects.filter(race__event=event)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)


class RaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for races.
    """

    queryset = Race.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RaceSerializer

    @action(detail=True, methods=["get"], url_path="results")
    def results(self, request, pk=None):
        race = self.get_object()
        results = Result.objects.filter(race=race)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)


class ResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint for results.
    """

    queryset = Result.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ResultSerializer
