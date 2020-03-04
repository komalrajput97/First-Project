from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^index/', index,name="index"),
    url(r'^getmenuitems/',get_menu_items,name="get_menu_items"),
    url(r'^getoutletfrompincode/',get_outlet_from_pincode,name="get_outlet_from_pincode"),
    url(r'^track_order/',track_order,name="track_order"),
    url(r'^add_to_cart/(?P<item_id>[0-9]+)/$', add_to_cart, name='add_to_cart'),
    url(r'^view_cart/', view_cart, name='view_cart'),
    url(r'^removefromcart/', remove_item_from_cart, name='remove_item_from_cart'),
    url(r'^updatecart/', update_quantity_in_cart, name='update_quantity_in_cart'),
    url(r'^checkout/', checkout, name='checkout'),
]   
