from django.db.models.signals import pre_save
from django.dispatch import receiver

from app.models import Product


@receiver(pre_save, sender=Product)
def set_default_values(sender, instance, **kwargs):
    print(1)
