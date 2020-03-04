# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(MenuCategory)
admin.site.register(HotelOutlet)
admin.site.register(HotelOutletGallery)
admin.site.register(MenuItem)

class OrderAdmin(admin.ModelAdmin):
	model = Order
	list_display = [booking.name for booking in Order._meta.fields]

admin.site.register(Order,OrderAdmin)

admin.site.register(OrderLine)