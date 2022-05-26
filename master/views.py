from django.shortcuts import redirect, render
from account.models import Account
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from store.models import product,Variation,VarientColor
from store.forms import AddProductForm,AddVariationForm
from account.decorators import unauthenticated_user,allowed_user

# Create your views here.


def admin_dashboard(request):
    products = product.objects.all()[0:6]

    context = {
        'products':products,
    }
    return render(request,'admin/admin_dashboard.html',context)


# ------adminLigin------

def admin_login(request):
    if request.method == 'POST':
        request.session['admin'] = 'admin'
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Account.objects.get(email=email)
        except:
            messages.error(request,'User does not exist,')
        
        user = authenticate(request,email=email,password=password)
        if user.is_superuser:
            if user is not None:
                login(request,user)
                return redirect('admin_dashboard')
            else:
                messages.error(request,'Username or password does not exist..!')
        else:
            messages.error(request,'Unauthenticated Entry..!')

    return render(request,'admin/admin_login.html')

def admin_logout(request):
    if request.session.has_key('admin'):
    #     # del request.session['admin']
        logout(request)
        return redirect('admin_login')



@allowed_user(allowed_roles=['admin'])
def add_product(request):
    curr_user = request.user
    print(curr_user)
    user = Account.objects.get(id=curr_user.id)
    print(user)
    if request.method =='POST':
        form = AddProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user=user
            if len(request.FILES) != 0:
                product.image  = request.FILES['image']
            product.save()
            messages.success(request,'product added Successfully')
            return redirect('add_product')
        else:
            print(form.errors)
            messages.info(request,"Something went wrong")
    form = AddProductForm()
    context = {'form':form}
    return render(request,'store/add_product.html',context)

@allowed_user(allowed_roles=['admin'])
def add_verient(request,pk):
    selected_product = product.objects.get(id=pk)
    if request.method == 'POST':
        form = AddVariationForm(request.POST,request.FILES)
        
        if form.is_valid():
            var = form.save(commit=False)
            var.product = selected_product
            if len(request.FILES) != 0:
                var.image1 = request.FILES['image1']
                var.image2 = request.FILES['image2']
                var.image3 = request.FILES['image3']
                var.image4 = request.FILES['image4']
            var.save()
            messages.success(request,'Variation saved Successfully')
            return redirect('list_product')
        else:
            print(form.errors)
            messages.info(request,"Somthing went wrong , Try again.")
            return redirect('list_product')
    form = AddVariationForm()
    context = {'form':form}

    return render(request,'store/add_variant.html',context)

@allowed_user(allowed_roles=['admin'])
def list_product(request):
    products = product.objects.all()

    context = {
        'products': products
    }
    return render(request,'store/list_product.html',context)

@allowed_user(allowed_roles=['admin'])
def view_product(request,pk):
    
    item = product.objects.get(id = pk)

    variants = Variation.objects.filter(product = pk)
    
    context = {
        'item':item,
        'variants':variants,
    }
    return render(request,'store/view_product.html', context )