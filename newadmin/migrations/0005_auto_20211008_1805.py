# Generated by Django 3.2.7 on 2021-10-08 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newadmin', '0004_auto_20211008_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='media/pics'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image1',
            field=models.ImageField(upload_to='media/pics'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image2',
            field=models.ImageField(upload_to='media/pics'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image3',
            field=models.ImageField(upload_to='media/pics'),
        ),
    ]
