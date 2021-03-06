# Generated by Django 3.2.7 on 2021-10-07 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, unique=True)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category_name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=250)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newadmin.category')),
            ],
        ),
        migrations.CreateModel(
            name='brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newadmin.category')),
                ('sub_category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newadmin.subcategory')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='brand_name',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='newadmin.brand'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='category_name',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='newadmin.category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='sub_catagory_name',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='newadmin.subcategory'),
            preserve_default=False,
        ),
    ]
