from django.contrib import admin
from events.models import Event, Result, Race

# Register your models here.
admin.site.register(Event)
admin.site.register(Race)
admin.site.register(Result)
