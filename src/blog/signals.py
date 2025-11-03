from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import NotificationPreference

from .models import BlogPost


@receiver(post_save, sender=BlogPost)
def send_announcement_created_email(sender, instance, created, **kwargs):
    if created:
        recipient_queryset = NotificationPreference.objects.filter(
            notification_type=NotificationPreference.BLOG_POST, enabled=True
        ).values_list("user__email", flat=True)
        recipient_list = list(recipient_queryset)
        msg = EmailMultiAlternatives(
            subject=f"New Fleet18 Blog Post: {instance.title}",
            body=(
                f"{instance.author.first_name} {instance.author.last_name} "
                f"made the following blog post:\n\n{instance.content}"
            ),
            from_email="blog@corychilton.com",
            to=recipient_list,
            # change to bcc in production
        )
        msg.send()
