from django.test import TestCase
from rest_framework.test import APIClient
from .models import Racer
from users.models import Racer
import datetime

class RacerTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        Racer.objects.create(
            first_name='Test1',
            last_name='Racer1'
        )
        Racer.objects.create(
            first_name='Test2',
            last_name='Racer2'
        )

    
    def test_model(self):
        racer = Racer.objects.get(pk=1)
        self.assertEqual(racer.first_name, 'Test1')
        self.assertEqual(racer.last_name, 'Racer1')

    def test_list(self):
        racers = self.c.get('/api/racers/').data
        self.assertEqual(len(racers), 2)

    def test_detail(self):
        racer = self.c.get('/api/racers/1/').data
        self.assertEqual(racer['last_name'], 'Racer1')
    
    def test_create(self):
        response = self.c.post('/api/racers/', {
            'first_name': 'Test3',
            'last_name': 'Racer3'
        })
        self.assertEqual(response.status_code, 201)
        racer = Racer.objects.get(pk=3)
        self.assertEqual(racer.first_name, 'Test3')
    
    def test_delete(self):
        response = self.c.delete('/api/racers/1/')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Racer.DoesNotExist):
            Racer.objects.get(pk=1)
    
    def test_duplicate_racer(self):
        response = self.c.post('/api/racers/', {
            'first_name': 'Test1',
            'last_name': 'Racer1'
        })
        self.assertEqual(response.status_code, 400)
