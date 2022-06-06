from kinematicviscosity.models import ViscosityMJL
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


from .models import LotVG, VGrange

@receiver(post_save, sender=ViscosityMJL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            trylot = LotVG.objects.get(lot=ViscosityMJL.lot)
        except ObjectDoesNotExist:
            trylot = None

        try:
            tryname = VGrange.objects.get(name=ViscosityMJL.name)
        except ObjectDoesNotExist:
            tryname = None

        if not trylot:
            LotVG.objects.create(viscosity=instance)





