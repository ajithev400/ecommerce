from .models import Cart,CartItems
from cart.views import _cart_id
def counter(request):
    user = request.user
    if user.is_authenticated:
        cart_items = CartItems.objects.filter(user = user)
        count = cart_items.count()
    
    else:
        count = 0
    return dict(count=count)