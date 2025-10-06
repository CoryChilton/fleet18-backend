from .models import Announcement
from rest_framework import viewsets, permissions
from .serializers import AnnouncementSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for announcements.
    """
    queryset = Announcement.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AnnouncementSerializer

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Returns the N most recent non-expired announcements.

        Query Params:
        - n (int): Number of announcements to return.
        """
        n = int(request.GET.get('n', 3))
        now = timezone.now()
        announcements = Announcement.objects.filter(expiration_timestamp__gt=now).order_by('-created_timestamp')[:n]
        serializer = self.get_serializer(announcements, many=True)
        return Response(serializer.data)
        