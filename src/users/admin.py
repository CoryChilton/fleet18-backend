from django.contrib import admin

from users.models import Racer, User

# Register your models here.
admin.site.register(User)
admin.site.register(Racer)
