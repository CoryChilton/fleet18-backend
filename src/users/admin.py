from django.contrib import admin
from users.models import Person, User, Racer

# Register your models here.
admin.site.register(Person)
admin.site.register(User)
admin.site.register(Racer)