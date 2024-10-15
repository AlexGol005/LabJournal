from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
import tablib
from import_export.admin import ExportActionModelAdmin, ExportMixin, ImportMixin


# реестр  классы для отображения в админке

# класс для загрузки/выгрузки  типа/модификации
class MeasurEquipmentCharaktersResource(ExportMixin, ImportMixin, resources.ModelResource):
    to_encoding = 'utf-8-sig'
    from_encoding = 'utf-8-sig'
    class Meta:
        model = MeasurEquipmentCharakters
        
# класс подробностей реестр 
class MeasurEquipmentCharaktersAdmin(ImportExportActionModelAdmin):
    resource_class = MeasurEquipmentCharaktersResource
    list_display = ('reestr', 'modificname', 'typename')
    search_fields = ['reestr',]
        
# фиксация формы в админке реестр 
admin.site.register(MeasurEquipmentCharakters, MeasurEquipmentCharaktersAdmin)

admin.site.register(Manufacturer)
admin.site.register(Rooms)
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


