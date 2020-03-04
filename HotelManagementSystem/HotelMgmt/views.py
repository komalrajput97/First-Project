# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from .forms import OrderPlacingForm
from .models import HotelOutletGallery, HotelOutlet, MenuItem, Order, OrderLine

# Create your views here.

def index(request):
    """
    Renders the index page
    """

    return render(request, "HotelMgmt/index.html")


def get_menu_items(request):
    """
    Returns the menu items of selected category
    """

    cat_id = request.POST.get('cat_id', None)
    menu_items = MenuItem.objects.filter(category_id=cat_id)
    context = {
        'menu_items': menu_items
    }
    menu_items_view = render_to_string('HotelMgmt/menu_items.html', context)

    return JsonResponse({'menu_items_view': menu_items_view})


def get_outlet_from_pincode(request):
    """
    Render details on index page based on pincode
    """

    pincode = request.POST.get('pincode', None)
    hotel_outlet_images = HotelOutletGallery.objects.filter(
        outlet__pincode=pincode)
    try:
        menu_categories = HotelOutlet.objects.get(
            pincode=pincode).menu_category.all()
        hotel_outlet_context = {
            'hotel_outlet_images': hotel_outlet_images,
        }
        hotel_outlet_images_view = render_to_string(
            'HotelMgmt/hotel_outlet_gallery.html', hotel_outlet_context)
        menu_categories_context = {
            'menu_categories': menu_categories,
        }
        menu_categories_view = render_to_string(
            'HotelMgmt/menu_categories.html', menu_categories_context)

    except HotelOutlet.DoesNotExist as e:
        return JsonResponse({'status':'fail','msg':str(e)})

    except Exception as e:
        return JsonResponse({'status':'fail','msg':str(e)})

    return JsonResponse({'status':'success','menu_categories_view': menu_categories_view, 'hotel_outlet_images_view': hotel_outlet_images_view, 'outlet_name': hotel_outlet_images[0].outlet.name})


def add_to_cart(request, item_id):
    """
    Renders cart page
    """

    # here we have not done user mgmt so we always get admin in request.user
    order, created = Order.objects.get_or_create(user=request.user,status='N')

    orderitem, item_created = OrderLine.objects.get_or_create(
        menu_item_id=item_id, order=order)

    # update the quantity if add to cart clicked again
    if not item_created:
        orderitem.quantity += 1
        orderitem.save()

    return redirect('view_cart')


def view_cart(request):
    """
    Function for displaying cart page
    """

    try:
        cart = Order.objects.get(user=request.user,status='N')
        if cart is not None:
            cart_list = OrderLine.objects.filter(order=cart)

            # calculate total
            total=0
            for cart_item in cart_list:
                total+=cart_item.menu_item.price*cart_item.quantity

            return render(request, "HotelMgmt/cart.html", {'cart_list': cart_list})
    except Exception as e:
        print(str(e))
    return render(request, "HotelMgmt/cart.html")


def update_quantity_in_cart(request):
    """
    Function for updating quantity of cart item
    """

    try:
        cart_item_id = request.POST.get("cart_item_id")
        operation = request.POST.get("operation")
        cart_item = OrderLine.objects.get(id=cart_item_id)
        if operation == "minus":
            cart_item.quantity -= 1
        elif operation == "plus":
            cart_item.quantity += 1
        elif operation == "quantity":
            cart_item.quantity = request.POST.get("quantity")
        cart_item.save()

        cart = Order.objects.get(user=request.user)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'fail','msg':str(e)})


def remove_item_from_cart(request):
    """
    Function for removing an item from cart item table
    """

    try:
        cart_item_id = request.POST.get("cart_item_id")
        # get item from item id
        del_cart_item = OrderLine.objects.get(id=cart_item_id)

        if del_cart_item is not None:

            # delete orderline item
            del_cart_item.delete()
            cart = Order.objects.get(id=del_cart_item.order.id)
            return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'fail','msg':str(e)})


def track_order(request):
    """
    Returns status of order
    """

    if request.method=="POST":
        token=request.POST.get('token',None)
        try:
            if token is not None:
                # check if token exists
                order = Order.objects.get(token=token)

                # get_status_display is inbuilt function to display value of choices field where status is field name default syntax get_fieldname_display()
                return JsonResponse({'status': 'success', 'order_status': order.get_status_display()})
        except Order.DoesNotExist:

            # if token does not exists return failure
            return JsonResponse({'status': 'fail','msg':str(e)})

        except Exception as e:
            return JsonResponse({'status': 'fail','msg':str(e)})

    else:
        return render(request, 'HotelMgmt/track_order.html')


def checkout(request):
    """
    Renders the checkout page
    """
    
    try:
        order=Order.objects.get(user=request.user,status='N')
        if request.method=="POST":

            # bind order object so that new object is not created when save method of form is called
            order_form=OrderPlacingForm(request.POST,instance=order)
            if order_form.is_valid():

                # update values in existing order by values entered by user in form
                saved_order=order_form.save()
                saved_order.token=get_random_string(10,'0123456789')

                # set order status as Preparing
                saved_order.status='P'
                saved_order.save()

                # delete entries from orderline table
                OrderLine.objects.filter(order_id=saved_order.id).delete()

                # when order is placed successfully,redirect to order details page
                return render(request,'HotelMgmt/order_details.html',{'order_details':saved_order})

        else:
            if order is not None:
                
                if OrderLine.objects.filter(order_id=order.id):
                    order_form=OrderPlacingForm()

                # if order exists but there are no items
                else:
                   return render(request,'HotelMgmt/checkout.html',{'msg':False}) 
    except Order.DoesNotExist:
        return render(request,'HotelMgmt/checkout.html',{'msg':False})

    return render(request,'HotelMgmt/checkout.html',{'order_form':order_form,'msg':True})


