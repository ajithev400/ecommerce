
from store.models import Variation,product
from category.models import category,sub_category
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q

# Create your views here.
def shop(request):
    cate = request.GET.get('cate') if request.GET.get('cate') != None else ''
    products = Variation.objects.filter(
        Q(product__category__category_name__icontains=cate) |
        Q(sub_category__sub_category_name__icontains=cate)
    )
    paginator = Paginator(products,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    categories = category.objects.all()
    sub_cate = sub_category.objects.all()[::-1]
    context = {
        'products':paged_products,
        'product_count':product_count,
        'categories':categories,
        'sub_cate':sub_cate,
    }
    return render(request,'store/shop.html',context)