from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import NotificationPreference

from .models import Announcement


@receiver(post_save, sender=Announcement)
def send_announcement_created_email(sender, instance, created, **kwargs):
    if created:
        recipient_queryset = NotificationPreference.objects.filter(
            notification_type=NotificationPreference.ANNOUNCEMENT, enabled=True
        ).values_list("user__email", flat=True)

        recipient_list = list(recipient_queryset)
        msg = EmailMultiAlternatives(
            subject=f"New Fleet18 Announcement: {instance.title}",
            body=(
                f"{instance.user.first_name} {instance.user.last_name} "
                f"made the following announcement:\n\n{instance.content}"
            ),
            from_email="announcements@corychilton.com",
            to=recipient_list,
            # change to bcc in production
        )
        msg.send()
