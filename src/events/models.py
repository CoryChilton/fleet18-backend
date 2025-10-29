from django.db import models
from users.models import Racer
from django.core.validators import MinValueValidator

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    event_time = models.DateTimeField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    entry_fee = models.DecimalField(
        decimal_places=2,
        max_digits=6, 
        validators=[MinValueValidator(0)]
    )


class Race(models.Model):
    SLALOM = "SLALOM"
    COURSE = "COURSE"
    RACE_TYPE_CHOICES = {
        SLALOM: "Slalom",
        COURSE: "Course"
    }

    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    # which race it is within the event
    number = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=15, choices=RACE_TYPE_CHOICES)
    name = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'number'],
                name='unique_event_race_number'
            )
        ]


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

    race = models.ForeignKey(Race, on_delete=models.PROTECT)
    racer = models.ForeignKey(Racer, on_delete=models.PROTECT)
    position = models.PositiveSmallIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1)]
    )
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=FINISHED)


