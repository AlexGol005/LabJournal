from django.contrib import admin
from .models import Manufacturer, Rooms, \
    Equipment, Roomschange, Personchange, MeasurEquipment


admin.site.register(Manufacturer)
admin.site.register(Rooms)
admin.site.register(Equipment)
admin.site.register(Roomschange)
admin.site.register(Personchange)
admin.site.register(MeasurEquipment)


