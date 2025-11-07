import datetime

from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User

from .models import Announcement


# Create your tests here.
class AnnouncementTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        user = User.objects.create(
            username="testuser", password="testpassword", is_staff=True
        )
        self.c.force_authenticate(user=user)
        Announcement.objects.create(
            title="Test Announcement",
            user=user,
            content="test content",
            expiration_timestamp="2100-10-1T00:00:00Z",
        )
        Announcement.objects.create(
            title="Test Announcement 2",
            user=user,
            content="test content 2",
            expiration_timestamp="2100-10-1T00:00:00Z",
        )

    def test_model(self):
        user = User.objects.get(pk=1)
        announcement = Announcement.objects.get(pk=1)
        self.assertEqual(announcement.title, "Test Announcement")
        self.assertEqual(announcement.user, user)
        self.assertEqual(announcement.content, "test content")
        self.assertEqual(
            announcement.expiration_timestamp,
            datetime.datetime(2100, 10, 1, 0, 0, tzinfo=datetime.timezone.utc),
        )

    def test_list(self):
        announcements = self.c.get("/api/announcements/").data
        self.assertEqual(len(announcements), 2)

    def test_recent_list(self):
        announcements = self.c.get(
            "/api/announcements/recent/", query_params={"n": 1}
        ).data
        self.assertEqual(len(announcements), 1)
        self.assertEqual(announcements[0]["title"], "Test Announcement 2")

    def test_detail(self):
        announcement = self.c.get("/api/announcements/1/").data
        self.assertEqual(announcement["title"], "Test Announcement")

    def test_create(self):
        response = self.c.post(
            "/api/announcements/",
            {
                "title": "Test Announcement 3",
                "user": 1,
                "content": "test content 3",
                "expiration_timestamp": "2100-10-1T00:00:00Z",
            },
        )
        self.assertEqual(response.status_code, 201)
        announcement = Announcement.objects.get(pk=3)
        self.assertEqual(announcement.title, "Test Announcement 3")

    def test_delete(self):
        response = self.c.delete("/api/announcements/1/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Announcement.DoesNotExist):
            announcement = Announcement.objects.get(pk=1)

    def test_invalid_expiration_timestamp(self):
        response = self.c.post(
            "/api/announcements/",
            {
                "title": "Test Announcement 3",
                "user": 1,
                "content": "test content 3",
                "expiration_timestamp": "2000-10-1T00:00:00Z",
            },
        )
        self.assertEqual(response.status_code, 400)
