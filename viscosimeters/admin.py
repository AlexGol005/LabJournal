from django.contrib import admin
from .models  import  Viscosimeters, Kalibration, ViscosimeterType




@admin.register(ViscosimeterType)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):

    def test(self, obj: ViscosimeterType) -> str:
        return f"{(obj.pairNumber + obj.diameter)}"

    list_display = ('diameter', 'pairNumber', 'viscosity1000', 'range', 'type', 'intervalVerification', 'test')
    fields = (('range', 'diameter'), 'pairNumber', 'viscosity1000', 'type', 'intervalVerification')

#     readonly_fields = ('create_at', 'update_at')
    # вычисляемое поле - но как его отобразить при просмотре заполненных??
    # разрешить редактирование
    # list_editable = ("is_available",)
    # Поиск по выбранным полям
    search_fields = ['diameter', 'type', ]
    list_filter = ['diameter', 'type', 'viscosity1000']





admin.site.register(Viscosimeters)
admin.site.register(Kalibration)
