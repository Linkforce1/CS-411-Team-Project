# Register your models here.
from django.contrib import admin

from .models import Users, Rooms, Guest

admin.site.register(Users)
admin.site.register(Rooms)
admin.site.register(Guest)
