from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ViscosimetersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'viscosimeters'

    verbose_name = _("Вискозиметры")
