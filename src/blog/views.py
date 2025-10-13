from .models import BlogPost
from rest_framework import viewsets, permissions
from .serializers import BlogPostSerializer
from rest_framework.decorators import action

class BlogPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for announcements.
    """
    queryset = BlogPost.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = BlogPostSerializer