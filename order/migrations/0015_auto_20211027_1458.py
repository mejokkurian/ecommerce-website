# Generated by Django 3.2.7 on 2021-10-27 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_order_order_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordernumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_no', models.CharField(default=0, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_no',
        ),
    ]
