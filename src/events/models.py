from django.db import models
from users.models import Racer
from django.core.validators import MinValueValidator

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=150)
    event_time = models.DateTimeField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    entry_fee = models.DecimalField(
        decimal_places=2,
        max_digits=6, 
        validators=[MinValueValidator(0)]
    )

class Result(models.Model):
    FINISHED = "FIN"
    DID_NOT_FINISH = "DNF"
    DID_NOT_START = "DNS"
    DISQUALIFIED = "DSQ"
    STATUS_CHOICES = {
        FINISHED: "Finished",
        DID_NOT_FINISH: "DNF",
        DID_NOT_START: "DNS",
        DISQUALIFIED: "Disqualified"
    }

    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    racer = models.ForeignKey(Racer, on_delete=models.PROTECT)
    position = models.PositiveSmallIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1)]
    )
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=FINISHED)


