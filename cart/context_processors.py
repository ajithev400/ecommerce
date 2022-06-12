from .models import Cart,CartItems

def counter(request):
    user = request.user
    if user.is_authenticated:
        cart_items = CartItems.objects.filter(user = user)
        count = cart_items.count()
    else:
        count = 0
    return dict(count=count)