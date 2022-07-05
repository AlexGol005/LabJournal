from django.contrib import admin
from .models import *

admin.site.register(GKCS)

admin.site.register(GKCSrange)


@admin.register(LotGKCS)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(CVclorinesaltsGKCS)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'namelot')



