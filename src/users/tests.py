import datetime

from django.test import TestCase
from rest_framework.test import APIClient

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
        self.c.force_authenticate(user=admin_user)
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
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, "test1")
        self.assertEqual(user.first_name, "first1")
        self.assertEqual(user.last_name, "last1")
        self.assertEqual(user.email, "test1@test.com")
        self.assertEqual(user.racer.pk, 1)
        self.assertTrue(user.check_password("pass1"))
        self.assertFalse(user.check_password("test"))

    def test_list(self):
        users = self.c.get("/api/users/").data
        self.assertEqual(len(users), 2)

    def test_detail(self):
        user = self.c.get("/api/users/1/").data
        self.assertEqual(user["username"], "test1")

    def test_create(self):
        racer = Racer.objects.create(first_name="Test2", last_name="Racer2")
        response = self.c.post(
            "/api/users/",
            {
                "first_name": "first3",
                "last_name": "last3",
                "username": "test3",
                "password": "pass3",
                "password2": "pass3",
                "email": "test3@test.com",
                "racer": 2,
            },
        )
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=4)
        self.assertEqual(user.username, "test3")
        self.assertTrue(user.check_password("pass3"))
        self.assertFalse(user.check_password("test3"))

    def test_delete(self):
        response = self.c.delete("/api/users/1/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=1)

    def test_duplicate_username(self):
        response = self.c.post(
            "/api/users/",
            {
                "first_name": "first3",
                "last_name": "last3",
                "username": "test1",
                "password": "pass3",
                "password2": "pass3",
                "email": "test3@test.com",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_duplicate_email(self):
        response = self.c.post(
            "/api/users/",
            {
                "first_name": "first3",
                "last_name": "last3",
                "username": "test3",
                "password": "pass3",
                "password2": "pass3",
                "email": "test1@test.com",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_duplicate_racer(self):
        response = self.c.post(
            "/api/users/",
            {
                "first_name": "first3",
                "last_name": "last3",
                "username": "test3",
                "password": "pass3",
                "password2": "pass3",
                "email": "test3@test.com",
                "racer": 1,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_password_mismatch(self):
        response = self.c.post(
            "/api/users/",
            {
                "first_name": "first3",
                "last_name": "last3",
                "username": "test3",
                "password": "pass3",
                "password2": "pass2",
                "email": "test3@test.com",
            },
        )
        self.assertEqual(response.status_code, 400)
