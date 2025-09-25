from django.db import models
from users.models import User

# Create your models here.
class NotificationPreferences(models.Model):
    BLOG_POST = "BLOG"
    ANNOUNCEMENT = "ANNOUNCEMENT"
    EVENT_REMINDER = "EVENT_REMINDER"
    NOTIFICATION_TYPES = {
        BLOG_POST: "New blog posts",
        ANNOUNCEMENT: "New announcement",
        EVENT_REMINDER: "Event reminders"
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    enabled = models.BooleanField(default=False)

