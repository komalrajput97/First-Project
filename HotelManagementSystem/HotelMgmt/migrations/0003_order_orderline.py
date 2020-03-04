# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-16 09:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('HotelMgmt', '0002_menuitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('customer_name', models.CharField(max_length=70)),
                ('status', models.CharField(choices=[('N', 'New'), ('A', 'Accepted'), ('P', 'Preparing'), ('T', 'InTransit'), ('D', 'Delivered')], max_length=1)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_phone', models.IntegerField()),
                ('shipping_address', models.TextField()),
                ('billing_address', models.TextField()),
                ('token', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HotelMgmt.MenuItem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HotelMgmt.Order')),
            ],
        ),
    ]