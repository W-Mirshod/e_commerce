# Generated by Django 5.0.7 on 2024-07-20 21:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0012_alter_customer_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 21, 2, 58, 10, 189624)),
        ),
    ]
