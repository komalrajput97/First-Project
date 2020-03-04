# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

# Create your models here.


class MenuCategory(models.Model):
    """
    Model for storing categories of menu in outlets
    """
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to="menu_categories")

    def __str__(self):
        return self.name


class HotelOutlet(models.Model):
    """
    Model for storing details of outlets of havmor outlets
    """

    name = models.CharField(max_length=50)
    pincode = models.IntegerField()
    address = models.TextField()
    contact_no = models.CharField(max_length=15)
    menu_category = models.ManyToManyField(MenuCategory)

    def __str__(self):
        return self.name


def outlet_directory_path(instance, filename):
    return 'hotel_outlets/{0}/{1}'.format(instance.outlet.name, filename)


class HotelOutletGallery(models.Model):
    """
    Model for storing gallery of hotel outlets
    """

    outlet = models.ForeignKey(HotelOutlet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=outlet_directory_path)

    def __str__(self):
        return self.outlet.name


class MenuItem(models.Model):
    """
    Model for storing menu items in particular menu category
    """

    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to='menu_items')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    """
    Model for storing order details
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=70, null=True)
    STATUS_CHOICES = (
        ('N', 'New'),
        ('A', 'Accepted'),
        ('P', 'Preparing'),
        ('T', 'InTransit'),
        ('D', 'Delivered'),
    )
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=1, default='N')
    customer_email = models.EmailField(null=True)
    customer_phone = models.IntegerField(null=True)
    shipping_address = models.TextField(null=True)
    billing_address = models.TextField(null=True)
    token = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str("{}:{}").format(self.user.username, self.get_status_display())


class OrderLine(models.Model):
    """
    Model for storing details of each item in order
    """

    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.menu_item.name
