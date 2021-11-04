# Generated by Django 3.2.9 on 2021-11-04 03:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Drama', 'Drama'), ('Self help books', 'Self help books'), ('Story books', 'Story Books'), ('Novels', 'Novels'), ('School books', 'School books'), ('Higher Education Books', 'Higher Education Books'), ('Other Books', 'Other Books')], max_length=200)),
                ('isbn', models.CharField(max_length=20)),
                ('pages', models.IntegerField()),
                ('price', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('additional_information', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads')),
                ('status', models.BooleanField(default=True)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_tag', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('Clothes', (('MW', "Men's wear"), ('WW', "Women's wear"), ('CD', "Kid's wear"))), ('Shoes', (('RS', 'Running Shoes'), ('FS', 'Formal Shoes'), ('SS', 'sneakers'), ('BS', 'Boots'), ('OS', 'Others'))), ('Electronics', (('LP', 'Laptop'), ('M', 'Mobile'), ('CM', 'Computor Parts'), ('O', 'Other'))), ('Stationery', (('PS', 'Pencils'), ('PN', 'Pens'), ('CS', 'Copies'), ('OT', 'Other Stationeries'))), ('Electrics', (('FE', 'Fans'), ('CE', 'Cables'), ('TE', ' Thin wires'), ('LE', 'LED'), ('TV', 'Television'), ('BE', 'Batteries'), ('OE', 'Other Electric materials'))), ('Other', 'Other')], max_length=255)),
                ('price', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('additional_information', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads')),
                ('status', models.BooleanField(default=True)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='SkartUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('mobile_number', models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(9999999999), django.core.validators.MinValueValidator(1000000000)])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(max_length=255, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
