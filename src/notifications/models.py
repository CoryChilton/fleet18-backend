from django.db import models

from users.models import User


# Create your models here.
class NotificationPreference(models.Model):
    BLOG_POST = "BLOG"
    ANNOUNCEMENT = "ANNOUNCEMENT"
    EVENT_REMINDER = "EVENT_REMINDER"
    NOTIFICATION_TYPES = {
        BLOG_POST: "New blog posts",
        ANNOUNCEMENT: "New announcement",
        EVENT_REMINDER: "Event reminders",
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    enabled = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "notification_type"],
                name="unique_user_notification_type",
            )
        ]

    def __str__(self):
        return f"{self.user}, {self.notification_type}, {self.enabled}"
