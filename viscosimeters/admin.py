from django.contrib import admin
from .models  import Status, ViscosimeterType, Manufacturer, Viscosimeters, Kalibration

admin.site.register(Manufacturer)
admin.site.register(Status)
admin.site.register(ViscosimeterType)
admin.site.register(Viscosimeters)
admin.site.register(Kalibration)
