from datetime import datetime
from zoneinfo import ZoneInfo

from django.utils import timezone
from PIL import ExifTags, Image
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import EventPhoto
from .serializers import EventPhotoSerializer


class EventPhotoViewSet(viewsets.ModelViewSet):
    """
    API endpoint for events.
    """

    queryset = EventPhoto.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EventPhotoSerializer

    def perform_create(self, serializer):
        photo_file = self.request.FILES.get("photo")
        photo_taken_timestamp = None

        if photo_file:
            try:
                photo = Image.open(photo_file)
                exif = photo.getexif()

                if exif:
                    exif_data = {
                        ExifTags.TAGS.get(k): v
                        for k, v in exif.items()
                        if k in ExifTags.TAGS
                    }

                    if "DateTime" in exif_data:
                        photo_taken_timestamp_str = exif_data["DateTime"]
                        photo_taken_timestamp = datetime.strptime(
                            photo_taken_timestamp_str, "%Y:%m:%d %H:%M:%S"
                        )
                        photo_taken_timestamp = photo_taken_timestamp.replace(
                            tzinfo=ZoneInfo("America/Los_Angeles")
                        )

            except Exception as e:
                print(f"EXIF read failed: {e}")

        if photo_taken_timestamp:
            serializer.save(photo_taken_timestamp=photo_taken_timestamp)
        else:
            serializer.save()
