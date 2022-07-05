from django.contrib import admin
from .models import*

admin.site.register(CommentsClorinesalts)
admin.site.register(TitrantHg)
admin.site.register(IndicatorDFK)


@admin.register(GetTitrHg)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(ClorinesaltsCV)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(Clorinesalts)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', )
