import os
import json
from root.settings import BASE_DIR
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from customers.models import Profile, Customer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Customer)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Falcon'
        context = {'customer': instance}
        html_message = render_to_string('auth/welcoming.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'noreply@falcon.com'
        to_email = instance.email

        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.send()

        print(f"Welcome email sent to {instance.email}")


@receiver(pre_delete, sender=Customer)
def archiving_deleted_users(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'customers/deleted_users', f"id-{instance.id}_{instance.full_name}.json")

    file_info = {
        'id': instance.id,
        'full_name': instance.full_name,
        'email': instance.email,
        'address': instance.address,
        'phone': instance.phone,
        'is_active': instance.is_active,
        'joined': str(instance.joined)}

    with open(file_path, 'w') as file:
        json.dump(file_info, file, indent=4)

    print(f"Product \"{instance.full_name}\" has deleted")
