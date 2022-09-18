from django.contrib import admin
from .models import*

# admin.site.register(ViscosityMJL)

@admin.register(Dinamicviscosity)
class NoteAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.performer = request.user
        super().save_model(request, obj, form, change)


@admin.register(CommentsDinamicviscosity)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)




