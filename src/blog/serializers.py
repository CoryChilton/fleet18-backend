from .models import BlogPost
from rest_framework import serializers
from django.utils import timezone

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'