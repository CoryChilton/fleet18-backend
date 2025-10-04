from .models import Announcement
from rest_framework import viewsets, permissions
from .serializers import AnnouncementSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AnnouncementSerializer