from .models import Event, Result
from rest_framework import viewsets, permissions
from .serializers import EventSerializer, ResultSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for events.
    """
    queryset = Event.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EventSerializer

    @action(detail=True, methods=['get'], url_path='results')
    def results(self, request, pk=None):
        event = self.get_object()
        results = Result.objects.filter(event=event)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

class ResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint for results.
    """
    queryset = Result.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ResultSerializer
