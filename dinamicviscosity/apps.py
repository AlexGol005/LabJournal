from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DinamicviscosityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dinamicviscosity'
    verbose_name = _("ЖА Вязкость динамическая, плотность")



