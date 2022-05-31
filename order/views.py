from django.shortcuts import render
from cart.models import CartItems
from .forms import OrderForm
from .models import Order,OrderProduct
import datetime
import razorpay
# Create your views here.
def place_order(request,total=0,quantity=0):
    user = request.user
    cart_items = CartItems.objects.filter(user=user)
    cart_count = cart_items.count()
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += int(cart_item.variant.price * cart_item.quantity)
        quantity += int(cart_item.quantity)
    tax = (2*total)/100
    grand_total = total+tax
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            print("Valid Order Form")
            data = Order()
            data.user = user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address1 = form.cleaned_data["address1"]
            data.address2 = form.cleaned_data["address2"]
            data.city = form.cleaned_data["city"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.pincode = form.cleaned_data["pincode"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()

            yr = int(datetime.date.today().strftime("%Y"))
            mt = int(datetime.date.today().strftime("%m"))
            dt = int(datetime.date.today().strftime("%d"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")

            payment_type = request.POST["payment"]

            currency = "INR"
            amount = grand_total * 100
            request.session["razorpay_amount"] = amount