from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for announcements.
    """

    queryset = BlogPost.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BlogPostSerializer
