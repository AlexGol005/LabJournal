from django.contrib import admin
from .models import*


admin.site.register(SSTN)

admin.site.register(SSTNrange)

@admin.register(LotSSTN)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(CVforSSTN)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'namelot')
