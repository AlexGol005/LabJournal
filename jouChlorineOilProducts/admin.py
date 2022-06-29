from django.contrib import admin
from .models import*


admin.site.register(CSN)

admin.site.register(CSNrange)

@admin.register(LotCSN)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(CVclorinesaltsCSN)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'namelot')
