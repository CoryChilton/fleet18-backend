import datetime

from django.test import TestCase
from rest_framework.test import APIClient

from users.models import Racer, User

from .models import Event, Race, Result


class EventTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        user = User.objects.create(
            username="testuser", password="testpassword", is_staff=True
        )
        self.c.force_authenticate(user=user)
        self.event1 = Event.objects.create(
            title="Test Event",
            event_time="2100-10-1T00:00:00Z",
            entry_fee=12.34,
            description="test event description",
            location="Leo Ryan Park",
        )
        self.event2 = Event.objects.create(
            title="Test Event 2",
            event_time="2101-10-1T00:00:00Z",
            entry_fee=20.00,
        )

    def test_model(self):
        event = self.event1
        self.assertEqual(event.title, "Test Event")
        self.assertEqual(
            event.event_time,
            "2100-10-1T00:00:00Z",
        )
        self.assertEqual(float(event.entry_fee), 12.34)
        self.assertEqual(event.description, "test event description")
        self.assertEqual(event.location, "Leo Ryan Park")

    def test_list(self):
        events = self.c.get("/api/events/").data
        self.assertEqual(len(events), 2)

    def test_detail(self):
        event = self.c.get(f"/api/events/{self.event1.id}/").data
        self.assertEqual(event["title"], "Test Event")

    def test_create(self):
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event 3",
                "event_time": "2100-10-1T00:00:00Z",
                "entry_fee": 123.45,
            },
        )
        self.assertEqual(response.status_code, 201)
        event = Event.objects.get(pk=response.data["id"])
        self.assertEqual(event.title, "Test Event 3")

    def test_delete(self):
        response = self.c.delete(f"/api/events/{self.event1.id}/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Event.DoesNotExist):
            Event.objects.get(pk=self.event1.id)

    def test_invalid_event_time(self):
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event 3",
                "event_time": "2000-10-1T00:00:00Z",
                "entry_fee": 123.45,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_entry_fee(self):
        response = self.c.post(
            "/api/events/",
            {
                "title": "Test Event 3",
                "event_time": "2100-10-1T00:00:00Z",
                "entry_fee": -1.00,
            },
        )
        self.assertEqual(response.status_code, 400)


class RaceTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        user = User.objects.create(
            username="testuser", password="testpassword", is_staff=True
        )
        self.c.force_authenticate(user=user)
        self.event = Event.objects.create(
            title="Test Event",
            event_time="2100-10-1T00:00:00Z",
            entry_fee=12.34,
        )
        self.race1 = Race.objects.create(
            event=self.event,
            number=1,
        )
        self.race2 = Race.objects.create(
            event=self.event,
            number=2,
        )

    def test_model(self):
        race = self.race1
        self.assertEqual(race.event_id, self.event.id)
        self.assertEqual(race.number, 1)
        self.assertEqual(race.type, Race.COURSE)
        self.assertEqual(race.name, None)

    def test_list(self):
        races = self.c.get("/api/races/").data
        self.assertEqual(len(races), 2)

    def test_detail(self):
        race = self.c.get(f"/api/races/{self.race1.id}/").data
        self.assertEqual(race["event"], self.event.id)
        self.assertEqual(race["number"], 1)

    def test_create(self):
        response = self.c.post(
            "/api/races/",
            {
                "event": self.event.id,
                "number": 3,
                "type": "MARATHON",
                "name": "test race",
            },
        )
        self.assertEqual(response.status_code, 201)
        race = Race.objects.get(pk=response.data["id"])
        self.assertEqual(race.name, "test race")
        self.assertEqual(race.type, Race.MARATHON)

    def test_delete(self):
        response = self.c.delete(f"/api/races/{self.race1.id}/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Race.DoesNotExist):
            Race.objects.get(pk=self.race1.id)

    def test_not_unique_event_race_number(self):
        response1 = self.c.post(
            "/api/races/",
            {
                "event": self.event.id,
                "number": 1,
            },
        )
        self.assertEqual(response1.status_code, 400)


class ResultTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        user = User.objects.create(
            username="testuser", password="testpassword", is_staff=True
        )
        self.c.force_authenticate(user=user)
        self.event = Event.objects.create(
            title="Test Event",
            event_time="2100-10-1T00:00:00Z",
            entry_fee=12.34,
        )
        self.race1 = Race.objects.create(
            event=self.event,
            number=1,
        )
        self.race2 = Race.objects.create(
            event=self.event,
            number=2,
        )
        self.racer = Racer.objects.create(first_name="Cory", last_name="Chilton")
        self.result1 = Result.objects.create(
            race=self.race1, racer=self.racer, position=1, status="FIN"
        )
        self.result2 = Result.objects.create(
            race=self.race2, racer=self.racer, position=5, status="DNF"
        )

    def test_model(self):
        result = self.result1
        self.assertEqual(result.race.pk, self.race1.id)
        self.assertEqual(result.racer.pk, self.racer.id)
        self.assertEqual(result.position, 1)
        self.assertEqual(result.status, "FIN")

    def test_list(self):
        results = self.c.get("/api/results/").data
        self.assertEqual(len(results), 2)

    def test_detail(self):
        results = self.c.get(f"/api/results/{self.result1.id}/").data
        self.assertEqual(results["race"], self.race1.id)

    def test_create(self):
        race3 = Race.objects.create(
            event=self.event,
            number=3,
        )
        response = self.c.post(
            "/api/results/",
            {
                "race": race3.id,
                "racer": self.racer.id,
                "status": "FIN",
                "position": 23,
            },
        )
        self.assertEqual(response.status_code, 201)
        result = Result.objects.get(pk=response.data["id"])
        self.assertEqual(result.position, 23)

    def test_delete(self):
        response = self.c.delete(f"/api/results/{self.result1.id}/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Result.DoesNotExist):
            Result.objects.get(pk=self.result1.id)

    def test_invalid_position(self):
        response1 = self.c.post(
            "/api/results/",
            {
                "race": self.race1.id,
                "racer": self.racer.id,
                "status": "FIN",
                "position": -1,
            },
        )
        self.assertEqual(response1.status_code, 400)
        response2 = self.c.post(
            "/api/results/",
            {
                "race": self.race1.id,
                "racer": self.racer.id,
                "status": "FIN",
                "position": 0,
            },
        )
        self.assertEqual(response2.status_code, 400)

    def test_invalid_status(self):
        response1 = self.c.post(
            "/api/results/",
            {
                "race": self.race1.id,
                "racer": self.racer.id,
                "status": "ABC",
                "position": 1,
            },
        )
        self.assertEqual(response1.status_code, 400)

    def test_invalid_racer(self):
        response1 = self.c.post(
            "/api/results/",
            {
                "race": self.race1.id,
                "racer": self.racer.id + 1,
                "status": "DNF",
                "position": 1,
            },
        )
        self.assertEqual(response1.status_code, 400)

    def test_invalid_race(self):
        response1 = self.c.post(
            "/api/results/",
            {
                "race": self.race2.id + 1,
                "racer": self.racer.id,
                "status": "DNF",
                "position": 1,
            },
        )
        self.assertEqual(response1.status_code, 400)

    def test_unique_racer_race(self):
        response = self.c.post(
            "/api/results/",
            {
                "race": self.race1.id,
                "racer": self.racer.id,
                "status": "DNF",
                "position": 1,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_event_results(self):
        event2 = Event.objects.create(
            title="Test Event 2",
            event_time="2100-10-1T00:00:00Z",
            entry_fee=12.34,
        )
        params1 = {"race__event": self.event.id}
        response1 = self.c.get("/api/results/", data=params1).data
        self.assertEqual(len(response1), 2)

        params2 = {"race__event": event2.id}
        response2 = self.c.get("/api/results/", data=params2).data
        self.assertEqual(len(response2), 0)

    def test_race_results(self):
        race3 = Race.objects.create(
            event=self.event,
            number=3,
        )
        params1 = {"race": self.race1.id}
        response1 = self.c.get("/api/results/", data=params1).data
        self.assertEqual(len(response1), 1)

        params2 = {"race": race3.id}
        response2 = self.c.get("/api/results/", data=params2).data
        self.assertEqual(len(response2), 0)

    def test_racer_results(self):
        racer2 = Racer.objects.create(first_name="Cory2", last_name="Chilton2")
        params1 = {"racer": self.racer.id}
        response1 = self.c.get("/api/results/", data=params1).data
        self.assertEqual(len(response1), 2)

        params2 = {"racer": racer2.id}
        response2 = self.c.get("/api/results/", data=params2).data
        self.assertEqual(len(response2), 0)
