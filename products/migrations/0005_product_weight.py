# Generated by Django 4.2.9 on 2024-08-03 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20240228_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
