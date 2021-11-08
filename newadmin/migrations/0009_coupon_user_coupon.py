# Generated by Django 3.2.7 on 2021-10-29 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newadmin', '0008_auto_20211010_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_rate', models.IntegerField()),
                ('coupon_code', models.CharField(max_length=50, unique=True)),
                ('percentage', models.PositiveIntegerField()),
                ('expiry_date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='user_coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('cpn_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newadmin.coupon')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
