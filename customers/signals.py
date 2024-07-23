import os
import json
from root.settings import BASE_DIR
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from customers.models import Profile, Customer


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_delete, sender=Customer)
def archiving_deleted_users(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'customers/deleted_users', "id-{instance.id}_{instance.full_name}.json")

    file_info = {
        'id': instance.id,
        'full_name': instance.full_name,
        'email': instance.email,
        'address': instance.address,
        'phone': instance.phone,
        'is_active': instance.is_active,
        'joined': str(instance.joined)
    }

    with open(file_path, 'w') as file:
        json.dump(file_info, file, indent=4)

    print(f"Product \"{instance.full_name}\" has deleted")
