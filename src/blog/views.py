from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from core.permissions import IsOwnerOrReadOnly

from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for announcements.
    """

    queryset = BlogPost.objects.all()
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    serializer_class = BlogPostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
