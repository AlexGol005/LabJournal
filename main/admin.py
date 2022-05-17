from django.contrib import admin
from .models import AttestationJ


@admin.register(AttestationJ)  # связываем админку с моделью
class AttestationJAdmin(admin.ModelAdmin):

    def test(self, obj: AttestationJ) -> str:
        return f"{obj.name}"
#

