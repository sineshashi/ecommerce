# Generated by Django 3.2.9 on 2021-11-11 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skcommeerce', '0005_auto_20211109_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='seller',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
