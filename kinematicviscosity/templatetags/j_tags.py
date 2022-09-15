from kinematicviscosity.j_constants import *
from django import template

register = template.Library()

@register.simple_tag()
def get_journal(get=None):
    return JOURNAL.objects.get(for_url=get)
