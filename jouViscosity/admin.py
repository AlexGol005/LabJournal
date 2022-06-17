from django.contrib import admin
from .models import*


admin.site.register(VG)
admin.site.register(CharacterVG)

admin.site.register(VGrange)

@admin.register(LotVG)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(CvKinematicviscosityVG)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id',)