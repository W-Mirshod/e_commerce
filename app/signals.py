import os
import json
from root.settings import BASE_DIR
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from app.models import Product


@receiver(pre_delete, sender=Product)
def archiving_deleted_products(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'app/deleted_products', f"{instance.id}_{instance.name}.json")

    product_info = {
        'id': instance.id,
        'name': instance.name,
        'description': instance.description,
        'ratings': instance.ratings,
        'favoured': instance.favoured,
        'add_to_cart': instance.add_to_cart,
        'discount': instance.discount
    }

    with open(file_path, 'w') as file:
        json.dump(product_info, file, indent=4)

    print(f"Product \"{instance.name}\" has deleted")
