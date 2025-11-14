from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User

from .models import NotificationPreference


class NotificationPreferenceTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        self.user = User.objects.create_user(
            username="test1",
            password="pass1",
            first_name="first1",
            last_name="last1",
            email="test1@test.com",
        )
        self.c.force_authenticate(user=self.user)
        self.pref1 = NotificationPreference.objects.create(
            user=self.user, notification_type="BLOG", enabled=True
        )
        self.pref2 = NotificationPreference.objects.create(
            user=self.user,
            notification_type="EVENT_REMINDER",
        )

    def test_model(self):
        pref = self.pref1
        self.assertEqual(pref.user.pk, self.user.id)
        self.assertEqual(pref.notification_type, "BLOG")
        self.assertTrue(pref.enabled)

    def test_list(self):
        prefs = self.c.get("/api/notification-preferences/").data
        self.assertEqual(len(prefs), 2)

    def test_detail(self):
        pref = self.c.get(f"/api/notification-preferences/{self.pref1.id}/").data
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
        pref = NotificationPreference.objects.get(pk=response.data["id"])
        self.assertEqual(pref.notification_type, "ANNOUNCEMENT")

    def test_delete(self):
        response = self.c.delete(f"/api/notification-preferences/{self.pref1.id}/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(NotificationPreference.DoesNotExist):
            NotificationPreference.objects.get(pk=self.pref1.id)

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
            self.assertEqual(pref["user"], self.user.id)
        # Switch to user 2
        self.c.force_authenticate(user=user2)
        response2 = self.c.get("/api/notification-preferences/").data
        self.assertEqual(len(response2), 1)
        for pref in response2:
            self.assertEqual(pref["user"], user2.id)
