from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import Announcement
from notifications.models import NotificationPreference

@receiver(post_save, sender=Announcement)
def send_announcement_created_email(sender, instance, created, **kwargs):
    if created:
        recipient_queryset = NotificationPreference.objects \
            .filter(notification_type=NotificationPreference.ANNOUNCEMENT, enabled=True) \
            .values_list('user__email', flat=True)
        
        recipient_list = list(recipient_queryset)
        msg = EmailMultiAlternatives(
            subject=f'Fleet18 Announcement: {instance.title}',
            body=f'{instance.author.first_name} {instance.author.last_name} made the following announcement:\n{instance.content}',
            from_email='announcements@corychilton.com',
            to=recipient_list
            # change to bcc in production
        )
        msg.send()
