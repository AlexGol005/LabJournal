from django.contrib.auth.models import User

from jouViscosity.models import CvKinematicviscosityVG
from kinematicviscosity.models import ViscosityMJL
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=ViscosityMJL)
def create_viscosityMJL(sender, instance, created, **kwargs):
    instance = CvKinematicviscosityVG.objects.get(namelot=ViscosityMJL.for_lot_and_name)
    if created:
        instance.update(cvt20=ViscosityMJL.certifiedValue_text)