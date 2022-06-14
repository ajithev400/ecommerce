from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from cart.models import CartItems
from store.models import Variation, VarientSize,product
from user.models import Address
from .forms import OrderForm
from .models import Order,OrderProduct,Payment
import datetime
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)

def payment(request):
    user = request.user
    body = json.loads(request.body)
    print(body)
    iorder = Order.objects.get(
        user = user, is_ordered=False, order_number=body["orderID"]
    )
    print(iorder)
    print(iorder.id)

    payment = Payment(
        user=user,
        payment_id=body["transID"],
        payment_method=body["payment_method"],
        amount_paid=iorder.order_total,
        status=body["status"],
    )
    payment.save()
    iorder.Payment = payment
    iorder.is_ordered = True
    iorder.save()

    cart_items = CartItems.objects.filter(
        user = user
    )
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = iorder.id
        orderproduct.payment = payment
        orderproduct.user_id = user.id
        orderproduct.products_id = item.varient.product.id
        orderproduct.variation_id = item.varient.id
        orderproduct.quantity = item.quantity

        orderproduct.price = item.varient.price
        orderproduct.ordered = True
        orderproduct.save()

        varient = Variation.objects.get(id = item.varient_id)
        print(varient)
        print(varient.stock)
        varient.stock -= item.quantity
        varient.save()
    CartItems.objects.filter(user = request.user).delete()
    data  = {
        "order_number": iorder.order_number,
        "trans_id": payment.payment_id,
    }
    return JsonResponse(data)



@login_required(login_url="login")
def place_order(request, total=0, quantity=0):
    user = request.user

    cart_items = CartItems.objects.filter(user = user)
    cart_count = cart_items.count()
    grand_total = 0
    tax = 0
    amount_pay = 0
    for cart_item in cart_items:
        total += int(cart_item.varient.product.price * cart_item.quantity)
    
    tax = (18*total)/100
    grand_total = tax + total

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()           
            data.user = user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address1 = form.cleaned_data["address1"]
            data.address2 = form.cleaned_data["address2"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.pincode = form.cleaned_data["pincode"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = grand_total
            data.tax = tax
            data.save()
            # generating order numbers
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            print(current_date)

            payment_type = request.POST['payment']
            currency = 'INR'
            amount = grand_total*100
            request.session["razorpay_amount"] = amount
            razorpay_order = razorpay_client.order.create(
                dict(amount=amount, currency=currency, payment_capture="0")
            )

            if payment_type == 'Razorpay':
                order_number = razorpay_order['id']
                data.order_number = razorpay_order['id']
                print('razor')
            else:
                order_number = current_date + str(data.id)
                print(data.id)
                data.order_number = order_number
                request.session['order_number'] = order_number
                print('cod')
            data.save()

            razorpay_order_id = razorpay_order['id']
            callback_url = "paymenthandler/"

            payment_type = request.POST['payment']
            print(payment_type)
            order = Order.objects.get(
                user = user, is_ordered=False, order_number=order_number
            )
            addresses = Address.objects.filter(user = request.user)
            
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,  
                'tax':tax,
                'grand_total':grand_total,
                'addresses':addresses,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_merchant_key': settings.RAZOR_KEY_ID,
                'razorpay_amount': amount,
                'currency': currency,
                'callback_url': callback_url,
                'amount_pay': amount_pay,
                'payment_type': payment_type,
            }
            return render(request,'payment.html',context)
    
        
        return redirect('checkout')




@csrf_exempt
def paymenthandler(request, total=0, quantity=0):
    user = request.user
    try:
        payment_id = request.POST.get('razorpay_payment_id', "")
        razorpay_order_id = request.POST.get("razorpay_order_id", "")
        signature = request.POST.get("razorpay_signature", "")
        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        }

        result = razorpay_client.utility.verify_payment_signature(
            params_dict
        )
        if result is not None:
            amount = request.session['razorpay_amount']
            try:
                razorpay_client.payment.capture(payment_id, amount)
                order = Order.objects.get(
                    user = user,
                    is_ordered=False,
                    order_number=razorpay_order_id,
                )

                payment = Payment(
                    user=user,
                    Payment_id=payment_id,
                    Payment_method="RazorPay",
                    amount_paid=order.order_total,
                    status="Completed",
                )
                payment.save()
                order.user = user
                order.Payment = payment
                order.is_ordered = True
                order.save()

                cart_items = CartItems.objects.filter(
                    user = request.user
                )
                for item in cart_items:
                    orderproduct = OrderProduct()
                    orderproduct.order_id = order.id
                    orderproduct.payment = payment
                    orderproduct.user_id = request.user.id
                    orderproduct.products_id = item.varient.product_id
                    orderproduct.variation_id = item.varient_id
                    orderproduct.quantity = item.quantity
                    orderproduct.price = item.varient.product.price
                    orderproduct.ordered = True
                    orderproduct.save()
                    print('orderproduct saved')
                    # cart_item = CartItems.objects.get(id = item.id)
                    # product_variation = cart_item.varient.all()
                    orderproduct = OrderProduct.objects.get(
                        id = orderproduct.id
                    )
                    # orderproduct.variation.set(product_variation)
                    orderproduct.save() 
                    print('orderproduct saved 2')
                    # product = product.objects.get(id = item.product_id)
                    # product.stock = product.stock - item.quantity
                    # product.save()
                    product = VarientSize.objects.get(product = item.varient, size = item.size.size)
                    product.stock = product.stock - item.quantity
                    product.save()
                    print('cod try block exicuted reduce the quantity of sold product')
                    # clear the cart
                    CartItems.objects.filter(user=request.user).delete()
                    request.session["order_number"]=razorpay_order_id
                    request.session["payment_id"] = payment_id
                # send transaction successfull
                # param = (
                #     "order_number="
                #     + order.order_number
                #     + "&payment_id="
                #     + payment.payment_id
                # )
                messages.success(request, "Payment Success")
                print("payment success")

                # redirect_url = reverse('order_complete')
                # return redirect(f'{redirect_url}?{param}')
                return redirect('order_complete')
                # render success page on successful caputre of payment
            except Exception as e:
                print(e)
                messages.error(request,'Payment Failed')

                return redirect('checkout')
        else:
            print('signature varification fails')
            return redirect('checkout')
            # if signature varification fails
    except:
        print('dont find the required parameters POST data')
        return redirect('checkout')
        # if don't find the required parameters in POST data
    # else:
    #     print("don't find the required parameters in POST data")
    #     return redirect('checkout')
        # if other than POST request is made

@login_required(login_url="login")
def cash_on_delivery(request):
    user = request.user
    order_number = request.session["order_number"]
    cart_items = CartItems.objects.filter(user = user)
    order = Order.objects.get(
        user = user, is_ordered=False, order_number=order_number
    )
    order = Order.objects.get(
        user=user, is_ordered=False, order_number=order_number
    )
    print(order)
    payment = Payment(
        user = user,
        Payment_id = order_number,
        Payment_method = "Cash On Delivery",
        amount_paid=order.order_total,
        status="Completed",
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.products_id = item.varient.product_id
        orderproduct.variation_id = item.varient_id
        orderproduct.quantity = item.quantity
        orderproduct.price = item.varient.product.price
        # orderproduct.product_price = item.varient.product.price
        orderproduct.ordered = True
        orderproduct.save()
        print('orderproduct saved')
        # cart_item = CartItems.objects.get(id = item.id)
        # product_variation = cart_item.varient.all()
        orderproduct = OrderProduct.objects.get(
            id = orderproduct.id
        )
        # orderproduct.variation.set(product_variation)
        orderproduct.save() 
        print('orderproduct saved 2')
        # product = product.objects.get(id = item.product_id)
        # product.stock = product.stock - item.quantity
        # product.save()
        product = VarientSize.objects.get(product = item.varient, size = item.size.size)
        product.stock = product.stock - item.quantity
        product.save()
        print('cod try block exicuted reduce the quantity of sold product')

        # clear the cart
        CartItems.objects.filter(user=request.user).delete()

    param = (
        "order_number="
        + order.order_number
        + "&payment_id="
        + payment.Payment_id
    )
    messages.success(request, "Payment Success")
    request.session["payment_id"] = payment.Payment_id
    # if "order_number" in request.session:
    #     del request.session["order_number"]
    # redirect_url = reverse("order_complete")
    # return redirect(f"{redirect_url}?{param}")
    return redirect('order_complete')

def order_complete(request):
    order_number = request.session['order_number']
    transID = request.session['payment_id']

    try:
        order = Order.objects.get(order_number= order_number, is_ordered=True)
        order_products = OrderProduct.objects.filter(order_id = order.id)
        
        subtotal = 0
        for i in order_products:
            subtotal += i.products.price * i.quantity

        payment = Payment.objects.get(Payment_id = transID)
        del request.session["order_number"]
        del request.session['payment_id']
        context = {
            'order':order,
            'order_products':order_products,
            'order_number':order_number,
            "transID": payment.Payment_id,
            "payment": payment,
            # "subtotal": subtotal,
        }
        return render(request, "user/order_complete.html", context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect("home")