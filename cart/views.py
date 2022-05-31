from multiprocessing import context
from statistics import quantiles
from urllib import request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

import user
from .models import Cart,CartItems,Wishlist
from store.models import Variation, VarientSize
from user.models import Address



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# ----add product to cart-----
def add_cart(request,product_id):
    
    current_user = request.user

    varient = Variation.objects.get(id=product_id)
    size = VarientSize.objects.get(product=varient)
    if current_user.is_authenticated:
        try: 
            cart_item = CartItems.objects.get(
                varient = varient,user = current_user
            )
            cart_item.quantity += 1
            cart_item.save()
        except CartItems.DoesNotExist:
            cart_item = CartItems.objects.create(
                varient = varient, 
                quantity = 1, 
                size=size,
                user = current_user
            )
            cart_item.save()
        return redirect('cart')
    
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        
        cart.save()

        try:
            cart_item = CartItems.objects.get(varient = varient, Cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItems.DoesNotExist:
            cart_item = CartItems.objects.create(
                varient=varient,
                quantity=1,
                Cart=cart,
                size = size
            )
            cart_item.save()
        return redirect("cart") 

def update_cart(request):

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        # print(product_id)
        if CartItems.objects.filter(user = request.user, varient_id = product_id):
            quantity = int(request.POST.get('quantity'))
            # print(quantity)
            cart = CartItems.objects.get( user = request.user, varient_id = product_id)
            cart.quantity = quantity
            cart.save()
            return JsonResponse('status',"Update successfully ")
    return redirect('home')

# -----cart-----
def cart(request, total=0, quantity=0, cart_items=None):

    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItems.objects.filter(
                user = request.user, is_active = True
            )
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItems.objects.filter(Cart= cart, is_active = True)

        for cart_item in cart_items:
            total += cart_item.varient.product.price * cart_item.quantity

            quantity += cart_item.quantity
        tax = (total * 2)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    
    return render(request,'cart/cart.html',context)

def delete_cart(request,product_id):
    current_user = request.user
    if current_user.is_authenticated:
        product = get_object_or_404(Variation, id = product_id)
        cart_item = CartItems.objects.get(varient = product, user = current_user)
        cart_item.delete()
        return redirect('cart')
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = get_object_or_404(Variation, id = product_id)
        cart_item = CartItems.objects.get(varient = product, Cart = cart)
        cart_item.delete()
        return redirect('cart')

def remove_cart(request, product_id):
    current_user = request.user
    if current_user.is_authenticated:
        variant = get_object_or_404(Variation, id = product_id)
        cart_item = CartItems.objects.get(varient = variant ,cart = cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')


def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try : 
        if request.user.is_authenticated:
            cart_items = CartItems.objects.filter(
                user = request.user, is_active=True
            )
            addresses = Address.objects.filter(user= request.user)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItems.objects.filter(cart = cart, is_active=True)

        for cart_item in cart_items:
            total = total = total+(
                cart_item.product.price * cart_item.quantity
            )
        tax = (2*total)/100
        grand_total = total+tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'addresses':addresses,
        
    }
    return render(request,'user/checkout.html',context)

def add_wishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            print(prod_id)
            
            product_check = Variation.objects.get(id = prod_id)
           
            if product_check:
                if Wishlist.objects.filter(user=request.user , variant_id = prod_id):
                    return JsonResponse({'status':"product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user , variant_id = prod_id)
                    return JsonResponse({'status':"product added to wishlist"})
            else:
                return JsonResponse({'status':"no such product found"})
        else:

            return JsonResponse({'status': "login to continue"})
    return redirect('home')

def wishlist(request):
    wishlist = Wishlist.objects.filter(user = request.user)
    context = {
        'wishlist':wishlist
    }
    return render(request,'user/wishlist.html',context)

# def add_wishlist(request,product_id):
#     if request.user.is_authenticated:
#         try :
#             product = Variation.objects.get(id = product_id)
#         except ObjectDoesNotExist:
#             pass

#         if product:
#             if Wishlist.objects.filter(user = request.user, variant_id = product_id):
#                 return JsonResponse({'status':"product already in wishlist"})
#             else:
#                 Wishlist.objects.create(user = request.user, variant_id = product_id)
#                 return JsonResponse({'status':"product added to wishlist"})
#         else:
#             return JsonResponse({'status':"no such product found"})
#     else:
#         return JsonResponse({'status': "login to continue"})