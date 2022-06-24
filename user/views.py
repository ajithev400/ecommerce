from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from account.forms import RegistrationForm
from account.models import Account
from account.otp import send_otp,verify_otp
from django.contrib.auth import authenticate,login,logout
from order.models import Order, OrderProduct
from user.forms import AddAdddressForm,UserProfileForm
from user.models import Address,Profile
from store.models import Variation,product,VarientSize
from cart.models import Cart, CartItems
from cart.views import _cart_id
from category.models import category
from account.decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required

def home(request):
    variations = Variation.objects.filter(is_available=True)[:10]
    categories = category.objects.all()
    products = product.objects.filter(is_available=True)
    context = {
        'variations':variations,
        'products':products,
        'categories':categories,
    }
    return render(request,'thedoo/index.html',context)

# --------userlogin--------
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Account.objects.get(email=email)
        except:
            messages.error(request,'User does not exist..!')
        
        user = authenticate(request,username=email,password=password)        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItems.objects.filter(Cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItems.objects.filter(Cart = cart)
                    print(cart_item)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                print('Except block activated.')
                pass

            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist..!')
        

    return render(request,'user/login.html')

# ------userRegistation-----   
def user_register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            gender = form.cleaned_data["gender"]
            mobile_number = form.cleaned_data["mobile"]
            password = form.cleaned_data["password"]    

            request.session["email"] = email
            request.session["mobile_number"] = mobile_number
            
            user=Account.objects.create_user(
                first_name = first_name,
                last_name= last_name,
                email= email,
                mobile = mobile_number,
                password = password, 
            )
            user.gender = gender
            profile = Profile()
            profile.first_name = first_name
            profile.last_name = last_name
            profile.user = user
            profile.gender = gender
            profile.phone = mobile_number
            profile.email = email
            profile.profile_picture = 'user/profile/profile.png'
            profile.save()
            user.save()
            send_otp(mobile_number)
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            print(mobile_number)

            return redirect('register_otp')
    
    form = RegistrationForm()
    context = {'form':form}
    return render(request,'register.html',context)


def register_otp(request):
    if request.method == 'POST':
        check_otp = request.POST.get('otpval')
        print(check_otp)
        mobile_number = request.session["mobile_number"]
        check = verify_otp(mobile_number,check_otp)
        if check:
            # messages.success(request, "Registered Successfully ! ")
            user = Account.objects.get(mobile = mobile_number)
            user.is_varified = True
            user.save()
            return redirect('home')
        else:
            messages.info(request,'Invalid OTP')
            return redirect('register_otp')
            
    return render(request,'otp_validation.html')

def resend_otp(request):
    mobile_number = request.session["mobile_number"]
    send_otp(mobile_number)
    return redirect('register_otp')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    orders = OrderProduct.objects.filter(user = request.user).order_by(
        'updated_at'
    )
    total_orders = orders.count()
    user_profile = Profile.objects.get(user = request.user.id)
    context = {
        'total_orders':total_orders,
        'user_profile':user_profile
    }
    return render(request,'user/dashboard.html',context)
    
def cart_list(request):

    return render(request,'cart/cart.html')


def product_details(request,product_slug,variant_slug):
    user = request.user
    newproducts = product.objects.all()
    
    try:
        single_variant = Variation.objects.get(
            product__slug =product_slug ,slug = variant_slug
        )
        if user.is_authenticated:
            in_cart = CartItems.objects.filter(
            varient = single_variant, user= user
            ).exists()
        else:
            in_cart = CartItems.objects.filter(
                varient = single_variant, Cart__cart_id=_cart_id(request)
            ).exists()
        # Cart__cart_id=_cart_id(request),
        size = VarientSize.objects.filter(
            product = single_variant
        )
        
        
    except Exception as e:
        raise e
    print(single_variant)
    variants = Variation.objects.filter(product = single_variant.product.id)
    context = {
        'single_variant':single_variant,
        'in_cart':in_cart,
        'variants':variants,
        'newproducts':newproducts,
        'size':size

    }

    return render(request,'thedoo/product_detail.html',context)

@login_required(login_url="login")
def user_address(request):
    if request.method == 'POST':
        form = AddAdddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            messages.success(request,'Address added Successfully')
            return redirect('user_address')
    address = Address.objects.filter(user = request.user)
    form = AddAdddressForm()
    context = {
        'form':form,
        'address':address
    }

    return render(request,'user/address.html',context)

@login_required(login_url="login")
def user_profile(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    form = UserProfileForm(instance=user_profile)
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,request.FILES,instance=user_profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated Successfully")
            return redirect('user_profile')
        else:
            print(form.errors)
    context = {
        'form':form,
        'user_profile':user_profile
    }
    return render( request, 'user/profile.html',context)

# -----list of user order and status----
@login_required(login_url="login")
def user_orders(request):
    user = request.user
    orders = OrderProduct.objects.filter(
        user = user, ordered=True
    ).order_by("-created_at")
    context = {
        'orders':orders
    }
    return render(request,'user/my_orders.html',context)


# ----user order details----
@login_required(login_url="login")
def order_detail(request, pk):
    user = request.user
    order_detail = OrderProduct.objects.filter(
        order__order_number= pk
    )
    order = Order.objects.get(user = user, order_number = pk)
    subtotal = 0
    for i in order_detail:
        subtotal = subtotal + i.price * i.quantity
    context = {
        "order_detail": order_detail,
        "order": order,
        "subtotal": subtotal,
    }
    return render(request,'user/order_detail.html',context)

# ---cancle-order---
@login_required(login_url="login")
def cancel_order(request, pk):

    order_product = OrderProduct.objects.get(id = pk)
    order_product.status = 'Canceled'
    order_product.save()
    product_id = order_product.products.id

    item = product.objects.get(pk = product_id)
    item.stock = item.stock+order_product.quantity
    return redirect('user_orders')

def error_404(request,exception):
    return render(request,'404.html')