from django.test import TestCase
from rest_framework.test import APIClient
from .models import Event, Result, Race
from users.models import Racer
import datetime


class EventTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        Event.objects.create(
            title='Test Event',
            event_time='2100-10-1T00:00:00Z',
            entry_fee=12.34,
            description='test event description',
            location='Leo Ryan Park'
        )
        Event.objects.create(
            title='Test Event 2',
            event_time='2101-10-1T00:00:00Z',
            entry_fee=20.00,
        )
    
    def test_model(self):
        event = Event.objects.get(pk=1)
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.event_time, datetime.datetime(2100, 10, 1, 0, 0, tzinfo=datetime.timezone.utc))
        self.assertEqual(float(event.entry_fee), 12.34)
        self.assertEqual(event.description, 'test event description')
        self.assertEqual(event.location, 'Leo Ryan Park')
    
    def test_list(self):
        events = self.c.get('/api/events/').data
        self.assertEqual(len(events), 2)

    def test_detail(self):
        event = self.c.get('/api/events/1/').data
        self.assertEqual(event['title'], 'Test Event')
    
    def test_create(self):
        response = self.c.post('/api/events/', {
            'title': 'Test Event 3',
            'event_time': '2100-10-1T00:00:00Z',
            'entry_fee': 123.45
        })
        self.assertEqual(response.status_code, 201)
        event = Event.objects.get(pk=3)
        self.assertEqual(event.title, 'Test Event 3')
    
    def test_delete(self):
        response = self.c.delete('/api/events/1/')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Event.DoesNotExist):
            Event.objects.get(pk=1)

    def test_invalid_event_time(self):
        response = self.c.post('/api/events/', {
            'title': 'Test Event 3',
            'event_time': '2000-10-1T00:00:00Z',
            'entry_fee': 123.45
        })
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_entry_fee(self):
        response = self.c.post('/api/events/', {
            'title': 'Test Event 3',
            'event_time': '2100-10-1T00:00:00Z',
            'entry_fee': -1.00
        })
        self.assertEqual(response.status_code, 400)


class RaceTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        event = Event.objects.create(
            title='Test Event',
            event_time='2100-10-1T00:00:00Z',
            entry_fee=12.34,
        )
        Race.objects.create(
            event=event,
            number=1,
        )
        Race.objects.create(
            event=event,
            number=2,
        )
    
    def test_model(self):
        race = Race.objects.get(pk=1)
        self.assertEqual(race.event_id, 1)
        self.assertEqual(race.number, 1)
        self.assertEqual(race.type, Race.COURSE)
        self.assertEqual(race.name, None)
    
    def test_list(self):
        races = self.c.get('/api/races/').data
        self.assertEqual(len(races), 2)

    def test_detail(self):
        race = self.c.get('/api/races/1/').data
        self.assertEqual(race['event'], 1)
        self.assertEqual(race['number'], 1)
    
    def test_create(self):
        response = self.c.post('/api/races/', {
            'event': 1,
            'number': 3,
            'type': 'MARATHON',
            'name': 'test race'
        })
        self.assertEqual(response.status_code, 201)
        race = Race.objects.get(pk=3)
        self.assertEqual(race.name, 'test race')
        self.assertEqual(race.type, Race.MARATHON)
    
    def test_delete(self):
        response = self.c.delete('/api/races/1/')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Race.DoesNotExist):
            Race.objects.get(pk=1)

    def test_not_unique_event_race_number(self):
        response1 = self.c.post('/api/races/', {
            'event': 1,
            'number': 1,
        })
        self.assertEqual(response1.status_code, 400)
    

class ResultTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        event = Event.objects.create(
            title='Test Event',
            event_time='2100-10-1T00:00:00Z',
            entry_fee=12.34,
        )
        race = Race.objects.create(
            event=event,
            number=1,
        )
        racer = Racer.objects.create(
            first_name='Cory',
            last_name='Chilton'
        )
        Result.objects.create(
            race=race,
            racer=racer,
            position=1,
            status='FIN'
        )
        Result.objects.create(
            race=race,
            racer=racer,
            position=5,
            status='DNF'
        )
    
    def test_model(self):
        result = Result.objects.get(pk=1)
        self.assertEqual(result.race.pk, 1)
        self.assertEqual(result.racer.pk, 1)
        self.assertEqual(result.position, 1)
        self.assertEqual(result.status, 'FIN')
    
    def test_list(self):
        results = self.c.get('/api/results/').data
        self.assertEqual(len(results), 2)

    def test_detail(self):
        results = self.c.get('/api/results/1/').data
        self.assertEqual(results['race'], 1)
    
    def test_create(self):
        response = self.c.post('/api/results/', {
            'race': 1,
            'racer': 1,
            'status': 'FIN',
            'position': 23,
        })
        self.assertEqual(response.status_code, 201)
        result = Result.objects.get(pk=3)
        self.assertEqual(result.position, 23)
    
    def test_delete(self):
        response = self.c.delete('/api/results/1/')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Result.DoesNotExist):
            Result.objects.get(pk=1)

    def test_invalid_position(self):
        response1 = self.c.post('/api/results/', {
            'race': 1,
            'racer': 1,
            'status': 'FIN',
            'position': -1,
        })
        self.assertEqual(response1.status_code, 400)
        response2 = self.c.post('/api/results/', {
            'race': 1,
            'racer': 1,
            'status': 'FIN',
            'position': 0,
        })
        self.assertEqual(response2.status_code, 400)
    
    def test_invalid_status(self):
        response1 = self.c.post('/api/results/', {
            'race': 1,
            'racer': 1,
            'status': 'ABC',
            'position': 1,
        })
        self.assertEqual(response1.status_code, 400)


    def test_invalid_racer(self):
        response1 = self.c.post('/api/results/', {
            'race': 1,
            'racer': 2,
            'status': 'DNF',
            'position': 1,
        })
        self.assertEqual(response1.status_code, 400)

    def test_invalid_event(self):
        response1 = self.c.post('/api/results/', {
            'race': 3,
            'racer': 1,
            'status': 'DNF',
            'position': 1,
        })
        self.assertEqual(response1.status_code, 400)

    def test_event_results(self):
        event = Event.objects.create(
            title='Test Event 2',
            event_time='2100-10-1T00:00:00Z',
            entry_fee=12.34,
        )
        response1 = self.c.get('/api/events/1/results/').data
        self.assertEqual(len(response1), 2)
        response2 = self.c.get('/api/events/2/results/').data
        self.assertEqual(len(response2), 0)

    def test_race_results(self):
        race = Race.objects.create(
            event_id=1,
            number=2,
        )
        response1 = self.c.get('/api/races/1/results/').data
        self.assertEqual(len(response1), 2)
        response2 = self.c.get('/api/races/2/results/').data
        self.assertEqual(len(response2), 0)

    def test_racer_results(self):
        racer = Racer.objects.create(
            first_name='Cory2',
            last_name='Chilton2'
        )
        response1 = self.c.get('/api/racers/1/results/').data
        self.assertEqual(len(response1), 2)
        response2 = self.c.get('/api/racers/2/results/').data
        self.assertEqual(len(response2), 0)
