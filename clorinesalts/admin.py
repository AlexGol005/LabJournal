from django.contrib import admin
from .models import*

admin.site.register(CommentsClorinesalts)
admin.site.register(IndicatorDFK)


@admin.register(TitrantHg)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'availablity')

@admin.register(GetTitrHg)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'lot', 'titr')

@admin.register(Clorinesalts)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index', 'lot', 'x1', 'x2', 'resultMeas', 'performer')





