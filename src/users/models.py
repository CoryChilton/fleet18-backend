from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)


class User(AbstractUser):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="user")


class Racer(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="racer")
