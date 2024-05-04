from django.contrib import admin
from .models import Receptionist, Guest, Room, Category, Reservation, Payment, HotelInfo


admin.site.register(Receptionist)
admin.site.register(Guest)
admin.site.register(Room)
admin.site.register(Category)
admin.site.register(Reservation)
admin.site.register(Payment)
admin.site.register(HotelInfo)
