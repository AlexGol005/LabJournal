from django.contrib import admin
from .models import *


# admin.site.register(ViscosityMJL)

@admin.register(ViscosityMJL)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    # exclude = ('performer',)  # скрыть performer поле, чтобы оно не отображалось в форме изменений

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.performer = request.user
        super().save_model(request, obj, form, change)
    # вычисляемое поле - но как его отобразить при просмотре заполненных??
    # def test(self, obj: ViscosityMJL) -> str:
    #     return f"{(obj.pairNumber + obj.diameter)}$"

    # list_display = ('total',)
    # fields = ('total',)

    # readonly_fields = ('create_at', 'update_at')
    # # разрешить редактирование
    # # list_editable = ("is_available",)
    # # Поиск по выбранным полям
    # search_fields = ['diameter', 'type', ]
    # list_filter = ['diameter', 'type', 'viscosity1000']


@admin.register(Comments)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)
