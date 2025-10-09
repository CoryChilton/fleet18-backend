from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Racer(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['first_name', 'last_name'],
                name='unique_first_last_name'
            )
        ]


class User(AbstractUser):
    racer = models.OneToOneField(Racer, on_delete=models.SET_NULL, related_name="user", null=True)



