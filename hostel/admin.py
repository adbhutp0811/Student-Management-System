from django.contrib import admin
from .models import Hostel, Room, RoomAllocation

admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(RoomAllocation)
