from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import IsAdminOrReadOnly

from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for announcements.
    """

    queryset = Announcement.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = AnnouncementSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """
        Returns the N most recent non-expired announcements.

        Query Params:
        - n (int): Number of announcements to return.
        """
        n = int(request.GET.get("n", 3))
        now = timezone.now()
        announcements = Announcement.objects.filter(
            expiration_timestamp__gt=now
        ).order_by("-created_timestamp")[:n]
        serializer = self.get_serializer(announcements, many=True)
        return Response(serializer.data)
