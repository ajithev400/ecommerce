from datetime import datetime
import string
from urllib import response
from winreg import REG_QWORD
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from account.models import Account
from order.models import Order,OrderProduct,STATUS1
from user.models import Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from store.models import product,Variation,VarientColor
from store.forms import AddProductForm,AddVariationForm
from account.decorators import unauthenticated_user,allowed_user
from django.template.loader import render_to_string
import tempfile
import csv
# import os

# os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")

# from weasyprint import HTML

# Create your views here.


@allowed_user(allowed_roles=['admin'])
def admin_dashboard(request):
    products = product.objects.all()
    # total_revenue = Order.objects.all().aggregate(sum("order_total"))
    total_order = Order.objects.filter(is_ordered=True).count()
    total_products = product.objects.filter(is_available=True).count()
    order_detail = OrderProduct.objects.filter(
        status = 'New'
    )

    # status
    new_count = OrderProduct.objects.filter(status="New").count()
    placed_count = OrderProduct.objects.filter(status="Placed").count()
    shipped_count = OrderProduct.objects.filter(status="Shipped").count()
    accepted_count = OrderProduct.objects.filter(
        status="Accepted"
    ).count()
    delivered_count = OrderProduct.objects.filter(
        status="Delivered"
    ).count()
    cancelled_count = OrderProduct.objects.filter(
        status="Canceled"
    ).count()

    users = Account.objects.all()
    profile = Profile.objects.all()
    context = {
        'products':products,
        'users':users,
        'profile':profile,
        'order_detail':order_detail,
        'total_order':total_order,
        'total_products':total_products,
        "status_counter": [
                new_count,
                placed_count,
                shipped_count,
                accepted_count,
                delivered_count,
                cancelled_count,
            ],
    }
    return render(request,'admin/admin_dashboard.html',context)

def admin_dashboard_old(request):
    products = product.objects.all()[0:6]
    users = Account.objects.all()
    profile = Profile.objects.all()

    context = {
        'products':products,
        'users':users,
        'profile':profile
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

# -----add new variant-----
@allowed_user(allowed_roles=['admin'])
def add_verient(request,pk):
    selected_product = product.objects.get(id=pk)
    if request.method == 'POST':
        form = AddVariationForm(request.POST,request.FILES)
        
        if form.is_valid():
            variant = form.save(commit=False)
            variant.product = selected_product
            if len(request.FILES) != 0:
                variant.image1 = request.FILES['image1']
                variant.image2 = request.FILES['image2']
                variant.image3 = request.FILES['image3']
                variant.image4 = request.FILES['image4']
            variant.save()
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



@allowed_user(allowed_roles=['admin'])
def edit_product(request,pk):
    edit_product = product.objects.get(id=pk)
    form = AddProductForm(instance=edit_product)
    if request.method == 'POST':
        form = AddProductForm(
            request.POST, request.FILES, instance = edit_product
        )
        if form.is_valid():
            form.save()
            messages.success(request, "product updated Successfully")
            return redirect('view-product',pk=pk)
        else:
            messages.info(request, "Something went wrong")
            return redirect("add_product")
    context = {
        'form':form
    }
    return render(request,'store/edit_product.html',context)


@allowed_user(allowed_roles=['admin'])
def delete_product(request,pk):
    product.objects.get(id=pk).delete()
    messages.success(request,'Product has been deleted')
    return redirect('list_product')

@allowed_user(allowed_roles=['admin'])
def activate_product(request, pk):
    selected_product = product.objects.get(id = pk)
    if selected_product.is_available:
        selected_product.is_available = False
        messages.success(request,"Done, product is not avilable now !")
    else:
        selected_product.is_available = True
        messages.success(request,"Done, product is Available !")
    selected_product.save()

    return redirect('list_product')


# ---edit variants----

@allowed_user(allowed_roles=['admin'])
def edit_variant(request,pk):
    edit_variant = Variation.objects.get(id = pk)
    form = AddVariationForm(instance = edit_variant)
    if request.method == 'POST':
        form = AddVariationForm(request.POST,request.FILES, instance= edit_variant)
        if form.is_valid():
            form.save()
            messages.success(request,'Variation updated Successfully')
            return redirect('list_product')
        else:
            messages.info(request,'somthing went wrong !')
            return redirect('edit_variant')
    context ={'form':form}
    return render(request,'store/edit_variant.html',context)


# ---activate variant---

@allowed_user(allowed_roles=['admin'])
def activate_variant(request,pk):
    selected_variant = Variation.objects.get(id = pk)
    if selected_variant.is_available:
        selected_variant.is_available = False
        messages.success(request, "Done, Product is not available now !")
    else:
        selected_variant.is_available = True
        messages.success(request, "Done, Product is available !")
    selected_variant.save()
    return redirect('list_product')

def customers(request):
    customers = Account.objects.all()
    context = {
        'customers':customers
    }
    return render(request,'admin/customers.html',context)

def customer_pickoff(request,pk):
    user = Account.objects.get(id=pk)
    if user.is_active:
        user.is_active = False
        user.is_rejectd = False
        messages.success(request, "Done, The User is Blocked !")
    else:
        user.is_active = True
        user.is_rejectd = True
        messages.success(request, "Done, user is Unblocked ")
    user.save()
    return redirect('customers')

@allowed_user(allowed_roles=['admin'])
def order_history(request):
    exclude_list = [
        "New",
        "Accepted",
        "Placed",
        "Shipped",
    ]
    active_orders = OrderProduct.objects.all()
    # .exclude(
    #     status__in=exclude_list
    # )[::-1]
    status = STATUS1
    context = {
        "active_orders": active_orders,
        "status": status,
    }
    return render(request,'admin/order-history.html',context)



@allowed_user(allowed_roles=['admin'])
def activeorders(request):
    exclude_list = ["Delivered", "Canceled"]
    active_orders = OrderProduct.objects.all().exclude(status__in=exclude_list)
    status = STATUS1
    context = {
        "active_orders": active_orders,
        "status": status,
    }
    return render(request, "admin/active_orders.html", context)

@allowed_user(allowed_roles=['admin'])
def order_status_change(request):
    pk = request.POST['id']
    status = request.POST["status"]
    order_product = OrderProduct.objects.get(id=pk)
    order_product.status = status
    order_product.save()
    return JsonResponse({"success": True})

@allowed_user(allowed_roles=['admin'])
def prouduct_report(request):
    products = product.objects.all()
    orders = OrderProduct.objects.filter(ordered=True).order_by("-created_at")

    if request.GET.get("from"):
        date_from = datetime.datetime.strptime(
            request.GET.get("from"), "%Y-%m-%d"
        )
        date_to = datetime.datetime.strptime(
            request.GET.get("to"), "%Y-%m-%d"
        )
        date_to += datetime.timedelta(days=1)
        orders = OrderProduct.objects.filter(
            created_at__range=[date_from, date_to]
        )

    if request.GET.get("from"):
        date_from = datetime.datetime.strptime(
            request.GET.get("from"), "%Y-%m-%d"
        )
        date_to = datetime.datetime.strptime(
            request.GET.get("to"), "%Y-%m-%d"
        )
        date_to += datetime.timedelta(days=1)
        products = product.objects.filter(
            created_date__range=[date_from, date_to]
        )

    context = {
        "products": products,
        "orders": orders,
    }
    return render(request, "admin/prouduct_report.html", context)

def order_export_pdf(request):
    pass
    # response = HttpResponse(content_type="application/pdf")
    # response[
    #     "Content-Disposition"
    # ] = "inline; attachement; filename=orders_Report"+\
    #     str(datetime.datetime.now())+".pdf"

    # response["Content-Transfer-Encoding"] = "binary"
    # orders = OrderProduct.objects.filter(ordered=True).order_by("-created_at")
    # html_string = render_to_string(
    #     "admin/orders_pdf_output.html", {"orders": orders, "total": 0}
    # )
    # # html = HTML(string = html_string)
    # result = html.write_pdf()
    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()
    #     output = open(output.name,'rb')
    #     response.write(output.read())

    # return response

def orders_export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=orders.csv"

    writer = csv.writer(response)
    orders = OrderProduct.objects.filter(ordered=True).order_by("-created_at")

    writer.writerow(
        [
            "Order Number",
            "Customer",
            "Product",
            "Amount",
            # "Payment",
            "Qty",
            "Status",
            "Date",
        ]
    )

    for order in orders:
        writer.writerow(
            [
                order.order.order_number,
                order.user.full_name(),
                order.products,
                order.price,
                # order.payment.Payment_method,
                order.quantity,
                order.status,
                order.updated_at,
            ]
        )
    return response