from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Racer(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"], name="unique_first_last_name"
            )
        ]


class User(AbstractUser):
    # username and password are always required
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False, unique=True)
    racer = models.OneToOneField(
        Racer, on_delete=models.SET_NULL, related_name="user", null=True, blank=True
    )
