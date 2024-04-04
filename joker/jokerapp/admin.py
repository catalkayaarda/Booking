from django.contrib import admin
from django.contrib.admin import site

from jokerapp.models import Room, Booking, User

# Register your models here.
site.register(Room)
site.register(Booking)
site.register(User)