from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User

from .models import NotificationPreference


class NotificationPreferenceTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        user = User.objects.create_user(
            username="test1",
            password="pass1",
            first_name="first1",
            last_name="last1",
            email="test1@test.com",
        )
        self.c.force_authenticate(user=user)
        NotificationPreference.objects.create(
            user=user, notification_type="BLOG", enabled=True
        )
        NotificationPreference.objects.create(
            user=user,
            notification_type="EVENT_REMINDER",
        )

    def test_model(self):
        pref = NotificationPreference.objects.get(pk=1)
        self.assertEqual(pref.user.pk, 1)
        self.assertEqual(pref.notification_type, "BLOG")
        self.assertTrue(pref.enabled)

    def test_list(self):
        prefs = self.c.get("/api/notification-preferences/").data
        self.assertEqual(len(prefs), 2)

    def test_detail(self):
        pref = self.c.get("/api/notification-preferences/1/").data
        self.assertEqual(pref["notification_type"], "BLOG")

    def test_create(self):
        response = self.c.post(
            "/api/notification-preferences/",
            {
                "notification_type": NotificationPreference.ANNOUNCEMENT,
                "enabled": True,
            },
        )
        self.assertEqual(response.status_code, 201)
        pref = NotificationPreference.objects.get(pk=3)
        self.assertEqual(pref.notification_type, "ANNOUNCEMENT")

    def test_delete(self):
        response = self.c.delete("/api/notification-preferences/1/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(NotificationPreference.DoesNotExist):
            NotificationPreference.objects.get(pk=1)

    def test_duplicate_user_notif_type(self):
        response = self.c.post(
            "/api/notification-preferences/",
            {
                "notification_type": NotificationPreference.BLOG_POST,
                "enabled": True,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_notif_type(self):
        response = self.c.post(
            "/api/notification-preferences/",
            {
                "notification_type": "TEST",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_user_specific_notif_prefs(self):
        user2 = User.objects.create_user(
            username="test2",
            password="pass1",
            first_name="first1",
            last_name="last1",
            email="test2@test.com",
        )
        NotificationPreference.objects.create(
            user=user2,
            notification_type="EVENT_REMINDER",
        )
        # Test as user 1 - should only see their own preferences
        response1 = self.c.get("/api/notification-preferences/").data
        self.assertEqual(len(response1), 2)
        for pref in response1:
            self.assertEqual(pref["user"], 1)
        # Switch to user 2
        self.c.force_authenticate(user=user2)
        response2 = self.c.get("/api/notification-preferences/").data
        self.assertEqual(len(response2), 1)
        for pref in response2:
            self.assertEqual(pref["user"], 2)
