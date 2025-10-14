from django.test import TestCase
from rest_framework.test import APIClient
from .models import NotificationPreference
from users.models import User

class NotificationPreferenceTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        user = User.objects.create_user(
            username='test1',
            password='pass1',
            first_name='first1',
            last_name='last1',
            email='test1@test.com'
        )
        NotificationPreference.objects.create(
            user=user,
            notification_type='BLOG',
            enabled=True
        )
        NotificationPreference.objects.create(
            user=user,
            notification_type='EVENT_REMINDER',
        )
    
    def test_model(self):
        pref = NotificationPreference.objects.get(pk=1)
        self.assertEqual(pref.user.pk, 1)
        self.assertEqual(pref.notification_type, 'BLOG')
        self.assertTrue(pref.enabled)
        

    def test_list(self):
        prefs = self.c.get('/api/notification_preferences/').data
        self.assertEqual(len(prefs), 2)

    def test_detail(self):
        pref = self.c.get('/api/notification_preferences/1/').data
        self.assertEqual(pref['notification_type'], 'BLOG')
    
    def test_create(self):
        response = self.c.post('/api/notification_preferences/', {
            'user': 1,
            'notification_type': NotificationPreference.ANNOUNCEMENT,
            'enabled': True
        })
        self.assertEqual(response.status_code, 201)
        pref = NotificationPreference.objects.get(pk=3)
        self.assertEqual(pref.notification_type, 'ANNOUNCEMENT')
    
    def test_delete(self):
        response = self.c.delete('/api/notification_preferences/1/')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(NotificationPreference.DoesNotExist):
            NotificationPreference.objects.get(pk=1)
    
    def test_duplicate_user_notif_type(self):
        response = self.c.post('/api/notification_preferences/', {
            'user': 1,
            'notification_type': NotificationPreference.BLOG_POST,
        })
        self.assertEqual(response.status_code, 400)

    def test_invalid_notif_type(self):
        response = self.c.post('/api/notification_preferences/', {
            'user': 1,
            'notification_type': 'TEST',
        })
        self.assertEqual(response.status_code, 400)

