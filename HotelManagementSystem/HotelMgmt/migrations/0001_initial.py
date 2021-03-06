# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-13 09:35
from __future__ import unicode_literals

import HotelMgmt.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HotelOutlet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('pincode', models.IntegerField()),
                ('address', models.TextField()),
                ('contact_no', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='HotelOutletGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=HotelMgmt.models.outlet_directory_path)),
                ('outlet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HotelMgmt.HotelOutlet')),
            ],
        ),
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('image', models.ImageField(upload_to='menu_categories')),
            ],
        ),
        migrations.AddField(
            model_name='hoteloutlet',
            name='menu_category',
            field=models.ManyToManyField(to='HotelMgmt.MenuCategory'),
        ),
    ]
