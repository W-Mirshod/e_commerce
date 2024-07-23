from django.db.models.signals import pre_save
from django.dispatch import receiver

from app.models import Product


@receiver(pre_save, sender=Product)
def set_default_values(sender, created, instance, **kwargs):
    if created:
        print(1)
