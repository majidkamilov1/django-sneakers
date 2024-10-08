# Generated by Django 5.0.6 on 2024-08-20 10:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakers', '0002_remove_sneaker_seller_cartitem_creator_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='sneaker',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_sneakers', to=settings.AUTH_USER_MODEL),
        ),
    ]
