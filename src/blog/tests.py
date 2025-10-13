from django.test import TestCase
from rest_framework.test import APIClient
from .models import BlogPost
from users.models import User, Racer
from events.models import Event
import datetime

# Create your tests here.
class BlogPostTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        racer = Racer.objects.create(
            first_name='Test1',
            last_name='Racer1'
        )
        user = User.objects.create_user(
            username='test1',
            password='pass1',
            first_name='first1',
            last_name='last1',
            email='test1@test.com',
            racer=racer
        )
        event = Event.objects.create(
            title='Test Event',
            event_time='2100-10-1T00:00:00Z',
            entry_fee=12.34,
        )
        BlogPost.objects.create(
            title='title1',
            author=user,
            content='content1',
            event=event
        )
        BlogPost.objects.create(
            title='title2',
            author=user,
            content='content2',
            event=event
        )
    

    def test_model(self):
        user = User.objects.get(pk=1)
        event = Event.objects.get(pk=1)
        blog_post = BlogPost.objects.get(pk=1)
        self.assertEqual(blog_post.title, 'title1')
        self.assertEqual(blog_post.author, user)
        self.assertEqual(blog_post.content, 'content1')
        self.assertEqual(blog_post.event, event)


    def test_list(self):
        blog_posts = self.c.get('/api/blog_posts/').data
        self.assertEqual(len(blog_posts), 2)
    

    def test_detail(self):
        blog_post = self.c.get('/api/blog_posts/1/').data
        self.assertEqual(blog_post['title'], 'title1')
    
    def test_create(self):
        response = self.c.post('/api/blog_posts/', {
            'title': 'title3',
            'author': 1,
            'content': 'content3',
            'event': 1
        })
        self.assertEqual(response.status_code, 201)
        blog_post = BlogPost.objects.get(pk=3)
        self.assertEqual(blog_post.title, 'title3')

    def test_delete(self):
        response = self.c.delete('/api/blog_posts/1/')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(BlogPost.DoesNotExist):
            announcement = BlogPost.objects.get(pk=1)

