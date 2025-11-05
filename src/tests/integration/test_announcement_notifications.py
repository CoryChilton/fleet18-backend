import time

from django.core import mail
from django.core.mail import send_mail
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from announcements.models import Announcement
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
        NotificationPreference.objects.create(
            user=user1,
            notification_type=NotificationPreference.ANNOUNCEMENT,
            enabled=True,
        )

    def test_user_receives_announcement_email_with_pref_on(self):
        response = self.c.post(
            "/api/announcements/",
            {
                "title": "Test Announcement",
                "author": 1,
                "content": "test content",
                "expiration_timestamp": "2100-10-1T00:00:00Z",
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, "announcements@corychilton.com")
        self.assertEqual(mail.outbox[0].to[0], "test1@test.com")

    def test_multiple_users_receive_announcement_emails(self):
        NotificationPreference.objects.create(
            user_id=2,
            notification_type=NotificationPreference.ANNOUNCEMENT,
            enabled=True,
        )
        response = self.c.post(
            "/api/announcements/",
            {
                "title": "Test Announcement",
                "author": 1,
                "content": "test content",
                "expiration_timestamp": "2100-10-1T00:00:00Z",
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue("test1@test.com" in mail.outbox[0].to)
        self.assertTrue("test2@test.com" in mail.outbox[0].to)

    def test_user_with_pref_off_does_not_receive_announcement_email(self):
        NotificationPreference.objects.update(
            user_id=1,
            notification_type=NotificationPreference.ANNOUNCEMENT,
            enabled=False,
        )
        response = self.c.post(
            "/api/announcements/",
            {
                "title": "Test Announcement",
                "author": 1,
                "content": "test content",
                "expiration_timestamp": "2100-10-1T00:00:00Z",
            },
        )
        self.assertEqual(len(mail.outbox), 0)
