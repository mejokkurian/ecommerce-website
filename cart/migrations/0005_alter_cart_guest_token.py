# Generated by Django 3.2.7 on 2021-11-06 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_cart_guest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='guest_token',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
