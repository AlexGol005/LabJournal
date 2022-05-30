from django.contrib import admin
from .models import Manufacturer, Rooms, MeasurEquipmentCharakters, Equipment

# Personchange, MeasurEquipment, , Roomschange,



admin.site.register(Manufacturer)
admin.site.register(Rooms)

# admin.site.register(Roomschange)

admin.site.register(MeasurEquipmentCharakters)
# admin.site.register(Personchange)
# admin.site.register(MeasurEquipment)
admin.site.register(Equipment)

