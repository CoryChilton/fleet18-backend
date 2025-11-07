import datetime
from zoneinfo import ZoneInfo

from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from notifications.models import NotificationPreference

from .models import Event


def send_event_reminders():
    """
    Sends reminders to all users that have opted in to event reminders for events
    happening tomorrow in PST.
    """
    pt = ZoneInfo("America/Los_Angeles")
    now_pt = timezone.now().astimezone(pt)
    start_of_tomorrow_pst = (now_pt + datetime.timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_of_tomorrow_pst = start_of_tomorrow_pst + datetime.timedelta(days=1)
    start_of_tomorrow_utc = start_of_tomorrow_pst.astimezone(datetime.timezone.utc)
    end_of_tomorrow_utc = end_of_tomorrow_pst.astimezone(datetime.timezone.utc)
    events = Event.objects.filter(
        event_time__gte=start_of_tomorrow_utc, event_time__lt=end_of_tomorrow_utc
    )
    recipient_queryset = NotificationPreference.objects.filter(
        notification_type=NotificationPreference.EVENT_REMINDER, enabled=True
    ).values_list("user__email", flat=True)
    recipient_list = list(recipient_queryset)
    for event in events:
        msg = EmailMultiAlternatives(
            subject=f"Fleet18 Event Reminder: {event.title}",
            body=(
                f"Reminder that {event.title} "
                f"is happening tomorrow:\nTime: {event.event_time}"
            ),
            from_email="event-reminder@corychilton.com",
            to=recipient_list,
            # change to bcc in production
        )
        msg.send()
