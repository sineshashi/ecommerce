# Generated by Django 3.2.9 on 2021-11-09 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skcommeerce', '0002_auto_20211107_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeorder',
            name='order_status',
            field=models.CharField(choices=[('Initialized', 'Initialized'), ('Dispatched', 'Dispatched'), ('On Route', 'On Route'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], default='Initialized', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Clothes', (('MW', "Men's wear"), ('WW', "Women's wear"), ('CD', "Kid's wear"))), ('Shoes', (('RS', 'Running Shoes'), ('FS', 'Formal Shoes'), ('SS', 'sneakers'), ('BS', 'Boots'), ('OS', 'Others'))), ('Electronics', (('LP', 'Laptop'), ('M', 'Mobile'), ('CM', 'Computor Parts'), ('O', 'Other'))), ('Stationery', (('PS', 'Pencils'), ('PN', 'Pens'), ('CS', 'Copies'), ('OT', 'Other Stationeries'))), ('Electrics', (('FE', 'Fans'), ('CE', 'Cables'), ('TE', ' Thin wires'), ('LE', 'LED'), ('TV', 'Television'), ('BE', 'Batteries'), ('OE', 'Other Electric materials'))), ('Books', (('Drama', 'Drama'), ('Self help books', 'Self help books'), ('Story books', 'Story Books'), ('Novels', 'Novels'), ('School books', 'School books'), ('Higher Education Books', 'Higher Education Books'), ('Other Books', 'Other Books'))), ('Other', 'Other')], max_length=255),
        ),
    ]
