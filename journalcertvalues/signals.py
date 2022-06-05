from kinematicviscosity.models import ViscosityMJL
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LotVG

@receiver(post_save, sender=ViscosityMJL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        LotVG.objects.create(viscosity=instance)
        LotVG.lot = ViscosityMJL.lot