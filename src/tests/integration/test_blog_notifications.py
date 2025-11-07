from django.core import mail
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from events.models import Event
from notifications.models import NotificationPreference
from users.models import User


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class BlogEmailTests(TestCase):
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
        # Authenticate as user1 for creating blog posts
        self.c.force_authenticate(user=user1)
        event = Event.objects.create(
            title="Test Event",
            event_time="2100-10-1T00:00:00Z",
            entry_fee=12.34,
        )
        NotificationPreference.objects.create(
            user=user1,
            notification_type=NotificationPreference.BLOG_POST,
            enabled=True,
        )

    def test_user_receives_blog_email_with_pref_on(self):
        response = self.c.post(
            "/api/blog_posts/",
            {"title": "title", "content": "content", "event": 1},
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, "blog@corychilton.com")
        self.assertEqual(mail.outbox[0].to[0], "test1@test.com")

    def test_multiple_users_receive_blog_emails(self):
        NotificationPreference.objects.create(
            user_id=2,
            notification_type=NotificationPreference.BLOG_POST,
            enabled=True,
        )
        response = self.c.post(
            "/api/blog_posts/",
            {"title": "title", "content": "content", "event": 1},
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue("test1@test.com" in mail.outbox[0].to)
        self.assertTrue("test2@test.com" in mail.outbox[0].to)

    def test_user_with_pref_off_does_not_receive_blog_email(self):
        NotificationPreference.objects.filter(
            user_id=1,
            notification_type=NotificationPreference.BLOG_POST,
        ).update(enabled=False)
        response = self.c.post(
            "/api/blog_posts/",
            {"title": "title", "content": "content", "event": 1},
        )
        self.assertEqual(len(mail.outbox), 0)
