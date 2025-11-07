from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.core import mail
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from events.cron import send_event_reminders
from events.models import Event
from notifications.models import NotificationPreference
from users.models import User


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class AnnouncementEmailTests(TestCase):
    def setUp(self):
        self.c = APIClient()
        user1 = User.objects.create_user(
            username="test1",
            password="pass1",
            first_name="first1",
            last_name="last1",
            email="test1@test.com",
        )
        user2 = User.objects.create_user(
            username="test2",
            password="pass2",
            first_name="first2",
            last_name="last2",
            email="test2@test.com",
        )
        # Create admin user for creating events
        admin_user = User.objects.create_user(
            username="admin",
            password="admin",
            first_name="admin",
            last_name="admin",
            email="admin@test.com",
            is_staff=True,
        )
        self.c.force_authenticate(user=admin_user)
        NotificationPreference.objects.create(
            user=user1,
            notification_type=NotificationPreference.EVENT_REMINDER,
            enabled=True,
        )

    def test_user_receives_event_reminder_email_with_pref_on(self):
        tom_iso_pt = (
            datetime.now(ZoneInfo("America/Los_Angeles")) + timedelta(days=1)
        ).isoformat()
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event",
                "event_time": tom_iso_pt,
                "entry_fee": 123.45,
            },
        )
        send_event_reminders()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, "event-reminder@corychilton.com")
        self.assertEqual(mail.outbox[0].to[0], "test1@test.com")

    def test_multiple_users_receive_event_reminder_emails(self):
        tom_iso_pt = (
            datetime.now(ZoneInfo("America/Los_Angeles")) + timedelta(days=1)
        ).isoformat()
        NotificationPreference.objects.create(
            user_id=2,
            notification_type=NotificationPreference.EVENT_REMINDER,
            enabled=True,
        )
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event",
                "event_time": tom_iso_pt,
                "entry_fee": 123.45,
            },
        )
        send_event_reminders()
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue("test1@test.com" in mail.outbox[0].to)
        self.assertTrue("test2@test.com" in mail.outbox[0].to)

    def test_user_with_pref_off_does_not_receive_event_reminder_email(self):
        tom_iso_pt = (
            datetime.now(ZoneInfo("America/Los_Angeles")) + timedelta(days=1)
        ).isoformat()
        NotificationPreference.objects.filter(
            user_id=1,
            notification_type=NotificationPreference.EVENT_REMINDER,
        ).update(enabled=False)
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event",
                "event_time": tom_iso_pt,
                "entry_fee": 123.45,
            },
        )
        send_event_reminders()
        self.assertEqual(len(mail.outbox), 0)

    def test_two_events_tomorrow(self):
        tom_iso_pt = (
            datetime.now(ZoneInfo("America/Los_Angeles")) + timedelta(days=1)
        ).isoformat()
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event",
                "event_time": tom_iso_pt,
                "entry_fee": 123.45,
            },
        )
        response2 = self.c.post(
            "/api/events/",
            {
                "title": "Test Event2",
                "event_time": tom_iso_pt,
                "entry_fee": 123.22,
            },
        )
        send_event_reminders()
        self.assertEqual(len(mail.outbox), 2)

    def test_event_in_two_days(self):
        in_two_days_iso_pt = (
            datetime.now(ZoneInfo("America/Los_Angeles")) + timedelta(days=2)
        ).isoformat()
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event",
                "event_time": in_two_days_iso_pt,
                "entry_fee": 123.45,
            },
        )
        send_event_reminders()
        self.assertEqual(len(mail.outbox), 0)

    def test_event_tomorrow_1201_am(self):
        tom_1201_am = (
            datetime.now(ZoneInfo("America/Los_Angeles")).replace(
                hour=0, minute=1, second=0, microsecond=0
            )
            + timedelta(days=1)
        ).isoformat()
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event",
                "event_time": tom_1201_am,
                "entry_fee": 123.45,
            },
        )
        send_event_reminders()
        self.assertEqual(len(mail.outbox), 1)

    def test_event_tomorrow_1159_pm(self):
        event_time = (
            datetime.now(ZoneInfo("America/Los_Angeles")).replace(
                hour=23, minute=59, second=0, microsecond=0
            )
            + timedelta(days=1)
        ).isoformat()
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event",
                "event_time": event_time,
                "entry_fee": 123.45,
            },
        )
        send_event_reminders()
        self.assertEqual(len(mail.outbox), 1)

    def test_event_in_two_days_1201_am(self):
        event_time = (
            datetime.now(ZoneInfo("America/Los_Angeles")).replace(
                hour=0, minute=1, second=0, microsecond=0
            )
            + timedelta(days=2)
        ).isoformat()
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event",
                "event_time": event_time,
                "entry_fee": 123.45,
            },
        )
        send_event_reminders()
        self.assertEqual(len(mail.outbox), 0)

    def test_event_today_1159_pm(self):
        event_time = (
            datetime.now(ZoneInfo("America/Los_Angeles")).replace(
                hour=23, minute=59, second=0, microsecond=0
            )
        ).isoformat()
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event",
                "event_time": event_time,
                "entry_fee": 123.45,
            },
        )
        send_event_reminders()
        self.assertEqual(len(mail.outbox), 0)
