from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import EventPhoto
from users.models import User
from events.models import Event
from django.core.files import File
import tempfile, shutil
import datetime

TEMP_MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class EventPhotoTestCase(TestCase):
    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.c = APIClient()
        user = User.objects.create_user(
            username='test1',
            password='pass1',
            first_name='first1',
            last_name='last1',
            email='test1@test.com',
        )
        event=Event.objects.create(
            title='Test Event 1',
            event_time='2101-10-1T00:00:00Z',
            entry_fee=20.00,
        )
        with open('tests/test_files/greek-fleet.JPG', 'rb') as f:
            EventPhoto.objects.create(
                photo=File(f),
                poster=user,
                caption='test caption',
                event=event,
            )

        with open('tests/test_files/windsurfer_logo.png', 'rb') as f:
            EventPhoto.objects.create(
                photo=File(f),
                poster=user,
                caption='test caption2',
                event=event,
            )


    def test_model(self):
        event_photo = EventPhoto.objects.get(pk=1)
        self.assertTrue(event_photo.photo.name.startswith('event_photos/'))
        self.assertTrue(event_photo.photo.storage.exists(event_photo.photo.name))
        self.assertEqual(event_photo.height, 750)
        self.assertEqual(event_photo.width, 1285)
        self.assertEqual(event_photo.poster_id, 1)
        self.assertEqual(event_photo.caption, 'test caption')
        self.assertEqual(event_photo.event_id, 1)
    

    def test_list(self):
        event_photos = self.c.get('/api/event-photos/').data
        self.assertEqual(len(event_photos), 2)


    def test_detail(self):
        event_photo = self.c.get('/api/event-photos/1/').data
        self.assertEqual(event_photo['caption'], 'test caption')
    

    def test_create(self):
        with open('tests/test_files/greek-fleet.JPG', 'rb') as f:
            response = self.c.post('/api/event-photos/', {
                'photo': File(f),
                'poster': 1,
                'caption': 'test create caption',
            },
            format='multipart')

        self.assertEqual(response.status_code, 201)
        event_photo = EventPhoto.objects.get(pk=3)
        self.assertEqual(event_photo.caption, 'test create caption')
        self.assertEqual(event_photo.height, 750)
        self.assertEqual(event_photo.width, 1285)
        # testing EXIF
        self.assertEqual(event_photo.photo_taken_timestamp, datetime.datetime.fromisoformat('2025-10-16 17:00:18+00:00'))


    def test_delete(self):
        response = self.c.delete('/api/event-photos/1/')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(EventPhoto.DoesNotExist):
            EventPhoto.objects.get(pk=1)

    def test_photo_taken_timestamp_no_exif(self):
        with open('tests/test_files/windsurfer_logo.png', 'rb') as f:
            response = self.c.post('/api/event-photos/', {
                'photo': File(f),
                'poster': 1,
                'caption': 'test create caption',
            },
            format='multipart')

        event_photo = EventPhoto.objects.get(pk=3)
        # self.assertEqual(event_photo.photo_taken_timestamp, event_photo.upload_timestamp)
        self.assertTrue(abs(event_photo.photo_taken_timestamp - event_photo.upload_timestamp).total_seconds() < 10)


