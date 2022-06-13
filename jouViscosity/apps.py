from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class JournalcertvaluesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jouViscosity'

    verbose_name = _('Журнал аттестованных значений: ВЖ-ПА')

