from django.contrib import admin
from .models  import Status, ViscosimeterType, Manufacturer, Viscosimeters, Kalibration

@admin.register(ViscosimeterType)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    # вычисляемое поле - но как его отобразить при просмотре заполненных??
    def test(self, obj: ViscosimeterType) -> str:
        return f"{(obj.pairNumber + obj.diameter)}$"

    list_display = ('diameter', 'pairNumber', 'viscosity1000', 'range', 'type', 'intervalVerification', 'test', 'create_at', 'update_at')
    fields = (('range', 'diameter'), 'pairNumber', 'viscosity1000', 'type', 'intervalVerification', 'create_at', 'update_at')

    readonly_fields = ('create_at', 'update_at')
    # разрешить редактирование
    # list_editable = ("is_available",)
    # Поиск по выбранным полям
    # search_fields = ['title', 'message', ]



admin.site.register(Manufacturer)
admin.site.register(Status)
# admin.site.register(ViscosimeterType)
admin.site.register(Viscosimeters)
admin.site.register(Kalibration)
