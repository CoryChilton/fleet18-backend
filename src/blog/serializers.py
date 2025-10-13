from .models import Blog
from rest_framework import serializers
from django.utils import timezone

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'