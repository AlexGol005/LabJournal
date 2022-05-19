from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ViscosityattestationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kinematicviscosity'

    verbose_name = _('Журнал определения кинематической вязкости ООО "Петроаналитика"')
