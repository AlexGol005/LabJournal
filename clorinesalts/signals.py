from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ClorinesaltsCV, Clorinesalts


@receiver(post_save, sender=Clorinesalts)
def create_cv(sender, instance, created, **kwargs):
    if created:
        ClorinesaltsCV.objects.create(clorinesalts=instance)



