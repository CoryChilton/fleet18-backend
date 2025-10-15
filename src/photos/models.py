from django.db import models
from users.models import User
from events.models import Event
from django.utils import timezone

# Create your models here.
class EventPhoto(models.Model):
    photo = models.ImageField(upload_to='event_photos/', height_field="height", width_field="width", unique=True)
    height = models.PositiveSmallIntegerField(blank=True)
    width = models.PositiveSmallIntegerField(blank=True)
    photo_taken_timestamp = models.DateTimeField(default=timezone.now)
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)