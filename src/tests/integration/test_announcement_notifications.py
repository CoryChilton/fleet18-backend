from django.core import mail
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from notifications.models import NotificationPreference
from users.models import User


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class AnnouncementEmailTests(TestCase):
    def setUp(self):
        self.c = APIClient()
        self.user1 = User.objects.create_user(
            username="test1",
            password="pass1",
            first_name="first1",
            last_name="last1",
            email="test1@test.com",
        )
        self.user2 = User.objects.create_user(
            username="test2",
            password="pass2",
            first_name="first2",
            last_name="last2",
            email="test2@test.com",
        )
        # Create admin user for creating announcements
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
            user=self.user1,
            notification_type=NotificationPreference.ANNOUNCEMENT,
            enabled=True,
        )

    def test_user_receives_announcement_email_with_pref_on(self):
        response = self.c.post(
            "/api/announcements/",
            {
                "title": "Test Announcement",
                "user": self.user1.id,
                "content": "test content",
                "expiration_timestamp": "2100-10-1T00:00:00Z",
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, "announcements@corychilton.com")
        self.assertEqual(mail.outbox[0].to[0], "test1@test.com")

    def test_multiple_users_receive_announcement_emails(self):
        NotificationPreference.objects.create(
            user=self.user2,
            notification_type=NotificationPreference.ANNOUNCEMENT,
            enabled=True,
        )
        response = self.c.post(
            "/api/announcements/",
            {
                "title": "Test Announcement",
                "user": self.user1.id,
                "content": "test content",
                "expiration_timestamp": "2100-10-1T00:00:00Z",
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue("test1@test.com" in mail.outbox[0].to)
        self.assertTrue("test2@test.com" in mail.outbox[0].to)

    def test_user_with_pref_off_does_not_receive_announcement_email(self):
        NotificationPreference.objects.filter(
            user=self.user1,
            notification_type=NotificationPreference.ANNOUNCEMENT,
        ).update(enabled=False)
        response = self.c.post(
            "/api/announcements/",
            {
                "title": "Test Announcement",
                "user": self.user1.id,
                "content": "test content",
                "expiration_timestamp": "2100-10-1T00:00:00Z",
            },
        )
        self.assertEqual(len(mail.outbox), 0)
