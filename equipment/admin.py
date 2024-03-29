from django.contrib import admin
from .models import *



admin.site.register(Manufacturer)
admin.site.register(Rooms)
admin.site.register(MeasurEquipmentCharakters)
admin.site.register(Personchange)
admin.site.register(MeasurEquipment)
admin.site.register(CommentsEquipment)
admin.site.register(Roomschange)
admin.site.register(VerificatorPerson)
admin.site.register(Verificators)
admin.site.register(DocsCons)
admin.site.register(CompanyCard)
admin.site.register(MeteorologicalParameters)
admin.site.register(TestingEquipmentCharakters)
admin.site.register(TestingEquipment)
admin.site.register(HelpingEquipment)
admin.site.register(HelpingEquipmentCharakters)

admin.site.register(ServiceEquipmentTE)
admin.site.register(ServiceEquipmentHE)


@admin.register(Verificationequipment)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ['equipmentSM__equipment__exnumber']

@admin.register(Attestationequipment)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ['equipmentSM__equipment__exnumber']


@admin.register(Checkequipment)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ['equipmentSM__equipment__exnumber']

@admin.register(Equipment)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ['exnumber']

@admin.register(ServiceEquipmentME)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ['charakters__name']


