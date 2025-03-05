# Generated by Django 5.1.6 on 2025-03-05 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('clothes', 'Одежда'), ('shoes', 'Обувь')], default='clothes', max_length=10),
        ),
        migrations.AddField(
            model_name='size',
            name='size_type',
            field=models.CharField(choices=[('clothes', 'Одежда'), ('shoes', 'Обувь')], default='clothes', max_length=10),
        ),
    ]
