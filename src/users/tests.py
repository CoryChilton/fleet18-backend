import datetime

from django.test import TestCase
from knox.models import AuthToken
from rest_framework.test import APIClient

from events.models import Event

from .models import Racer, User


class RacerTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        # Create admin user for write operations
        admin_user = User.objects.create_user(
            username="admin",
            password="admin",
            first_name="admin",
            last_name="admin",
            email="admin@test.com",
            is_staff=True,
        )
        self.c.force_authenticate(user=admin_user)
        Racer.objects.create(first_name="Test1", last_name="Racer1")
        Racer.objects.create(first_name="Test2", last_name="Racer2")

    def test_model(self):
        racer = Racer.objects.get(pk=1)
        self.assertEqual(racer.first_name, "Test1")
        self.assertEqual(racer.last_name, "Racer1")

    def test_list(self):
        racers = self.c.get("/api/racers/").data
        self.assertEqual(len(racers), 2)

    def test_detail(self):
        racer = self.c.get("/api/racers/1/").data
        self.assertEqual(racer["last_name"], "Racer1")

    def test_create(self):
        response = self.c.post(
            "/api/racers/", {"first_name": "Test3", "last_name": "Racer3"}
        )
        self.assertEqual(response.status_code, 201)
        racer = Racer.objects.get(pk=3)
        self.assertEqual(racer.first_name, "Test3")

    def test_delete(self):
        response = self.c.delete("/api/racers/1/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Racer.DoesNotExist):
            Racer.objects.get(pk=1)

    def test_duplicate_racer(self):
        response = self.c.post(
            "/api/racers/", {"first_name": "Test1", "last_name": "Racer1"}
        )
        self.assertEqual(response.status_code, 400)


class UserTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        # Create admin user for all operations (IsAdminUser requires admin for all)
        admin_user = User.objects.create_user(
            username="admin",
            password="admin",
            first_name="admin",
            last_name="admin",
            email="admin@test.com",
            is_staff=True,
        )
        instance, token = AuthToken.objects.create(admin_user)
        self.c.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        racer = Racer.objects.create(first_name="Test1", last_name="Racer1")
        User.objects.create_user(
            username="test1",
            password="pass1",
            first_name="first1",
            last_name="last1",
            email="test1@test.com",
            racer=racer,
        )
        User.objects.create_user(
            username="test2",
            password="pass2",
            first_name="first2",
            last_name="last2",
            email="test2@test.com",
        )

    def test_model(self):
        user = User.objects.get(pk=2)
        self.assertEqual(user.username, "test1")
        self.assertEqual(user.first_name, "first1")
        self.assertEqual(user.last_name, "last1")
        self.assertEqual(user.email, "test1@test.com")
        self.assertEqual(user.racer.pk, 1)
        self.assertTrue(user.check_password("pass1"))
        self.assertFalse(user.check_password("test"))

    def test_list(self):
        users = self.c.get("/api/users/").data
        self.assertEqual(len(users), 3)

    def test_detail(self):
        user = self.c.get("/api/users/2/").data
        self.assertEqual(user["username"], "test1")


class RegisterTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()

    def test_normal_register(self):
        response = self.c.post(
            "/api/auth/register/",
            {
                "first_name": "testfirst",
                "last_name": "testlast",
                "username": "testusername",
                "password": "testpassword",
                "password2": "testpassword",
                "email": "test@test.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response.data)

    def test_duplicate_username(self):
        self.c.post(
            "/api/auth/register/",
            {
                "first_name": "testfirst",
                "last_name": "testlast",
                "username": "testusername",
                "password": "testpassword",
                "password2": "testpassword",
                "email": "test@test.com",
            },
        )
        response = self.c.post(
            "/api/auth/register/",
            {
                "first_name": "testfirst2",
                "last_name": "testlast2",
                "username": "testusername",
                "password": "testpassword2",
                "password2": "testpassword2",
                "email": "test2@test.com",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_duplicate_email(self):
        self.c.post(
            "/api/auth/register/",
            {
                "first_name": "testfirst",
                "last_name": "testlast",
                "username": "testusername",
                "password": "testpassword",
                "password2": "testpassword",
                "email": "test@test.com",
            },
        )
        response = self.c.post(
            "/api/auth/register/",
            {
                "first_name": "testfirst2",
                "last_name": "testlast2",
                "username": "testusername2",
                "password": "testpassword2",
                "password2": "testpassword2",
                "email": "test@test.com",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_duplicate_racer(self):
        racer = Racer.objects.create(first_name="Test1", last_name="Racer1")
        User.objects.create_user(
            username="test1",
            password="pass1",
            first_name="first1",
            last_name="last1",
            email="test1@test.com",
            racer=racer,
        )
        response = self.c.post(
            "/api/auth/register/",
            {
                "first_name": "testfirst2",
                "last_name": "testlast2",
                "username": "testusername2",
                "password": "testpassword2",
                "password2": "testpassword2",
                "email": "test@test.com",
                "racer": 1,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_password_mismatch(self):
        response = self.c.post(
            "/api/auth/register/",
            {
                "first_name": "testfirst2",
                "last_name": "testlast2",
                "username": "testusername2",
                "password": "testpassword1",
                "password2": "testpassword2",
                "email": "test@test.com",
            },
        )
        self.assertEqual(response.status_code, 400)


class LoginTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        User.objects.create_user(
            username="test1",
            password="pass1",
            first_name="first1",
            last_name="last1",
            email="test1@test.com",
        )

    def test_normal_login(self):
        response = self.c.post(
            "/api/auth/login/",
            {
                "identifier": "test1",
                "password": "pass1",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response.data)
        self.assertTrue("expiry" in response.data)

    def test_wrong_password(self):
        response = self.c.post(
            "/api/auth/login/",
            {
                "username": "test1",
                "password": "pass2",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_non_existent_user(self):
        response = self.c.post(
            "/api/auth/login/",
            {
                "username": "test2",
                "password": "pass1",
            },
        )
        self.assertEqual(response.status_code, 400)


class LogoutTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        User.objects.create_user(
            username="test1",
            password="pass1",
            first_name="first1",
            last_name="last1",
            email="test1@test.com",
        )
        Event.objects.create(
            title="Test Event",
            event_time="2100-10-1T00:00:00Z",
            entry_fee=12.34,
            description="test event description",
            location="Leo Ryan Park",
        )

    def test_normal_logout(self):
        response1 = self.c.post(
            "/api/auth/login/",
            {
                "identifier": "test1",
                "password": "pass1",
            },
        )
        token = response1.data["token"]
        self.c.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response_blog1 = self.c.post(
            "/api/blog_posts/",
            {"title": "title1", "content": "content1", "event": 1},
        )
        self.assertEqual(response_blog1.status_code, 201)
        response2 = self.c.post("/api/auth/logout/")
        self.assertEqual(response2.status_code, 204)
        response3 = self.c.post("/api/auth/logout/")
        self.assertEqual(response3.status_code, 401)
        response_blog2 = self.c.post(
            "/api/blog_posts/",
            {"title": "title1", "content": "content1", "event": 1},
        )
        self.assertEqual(response_blog2.status_code, 401)

    def test_normal_logoutall(self):
        response1 = self.c.post(
            "/api/auth/login/",
            {
                "identifier": "test1",
                "password": "pass1",
            },
        )
        token1 = response1.data["token"]
        response2 = self.c.post(
            "/api/auth/login/",
            {
                "identifier": "test1",
                "password": "pass1",
            },
        )
        token2 = response2.data["token"]
        self.assertNotEqual(token1, token2)
        self.c.credentials(HTTP_AUTHORIZATION=f"Token {token1}")
        response_blog1 = self.c.post(
            "/api/blog_posts/",
            {"title": "title1", "content": "content1", "event": 1},
        )
        self.assertEqual(response_blog1.status_code, 201)
        self.c.credentials(HTTP_AUTHORIZATION=f"Token {token2}")
        response_blog1 = self.c.post(
            "/api/blog_posts/",
            {"title": "title1", "content": "content1", "event": 1},
        )
        self.assertEqual(response_blog1.status_code, 201)
        self.c.credentials(HTTP_AUTHORIZATION=f"Token {token1}")
        response3 = self.c.post("/api/auth/logoutall/")
        self.assertEqual(response3.status_code, 204)
        response_blog2 = self.c.post(
            "/api/blog_posts/",
            {"title": "title1", "content": "content1", "event": 1},
        )
        self.assertEqual(response_blog2.status_code, 401)
        self.c.credentials(HTTP_AUTHORIZATION=f"Token {token2}")
        response_blog3 = self.c.post(
            "/api/blog_posts/",
            {"title": "title1", "content": "content1", "event": 1},
        )
        self.assertEqual(response_blog3.status_code, 401)
