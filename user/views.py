from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from account.forms import RegistrationForm
from account.models import Account
from account.otp import send_otp,verify_otp
from django.contrib.auth import authenticate,login,logout
from user.models import Address,Profile, Roles
from store.models import Variation,product
from category.models import category
from account.decorators import unauthenticated_user

def home(request):
    variations = Variation.objects.filter(is_available=True)
    categories = category.objects.all()
    products = product.objects.all()
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
            profile.role = Roles.objects.get(group='customer')
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


def logout_user(request):
    logout(request)
    return redirect('login')


def cart_list(request):

    return render(request,'cart/cart.html')


def product_details(request,pk):

    item = product.objects.get(id = pk)
    variant = Variation.objects.all().filter(product=item)

    newproducts = product.objects.all()
    
    context = {
        'item':item,
        'variant':variant,
        'newproducts':newproducts
    }

    return render(request,'thedoo/product_detail.html',context)