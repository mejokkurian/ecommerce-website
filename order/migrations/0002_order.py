# Generated by Django 3.2.7 on 2021-10-15 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_cart_username'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15)),
                ('city', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=10)),
                ('payment_method', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=10)),
                ('total', models.CharField(max_length=15)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.cart')),
            ],
        ),
    ]