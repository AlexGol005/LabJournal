from django.contrib import admin
from .models import*

admin.site.register(Clorinesalts)
admin.site.register(CommentsClorinesalts)

admin.site.register(TitrantHg)
admin.site.register(IndicatorDFK)

@admin.register(GetTitrHg)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', )

