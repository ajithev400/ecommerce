from django.contrib import admin
from .models import Cart,CartItems,Wishlist

admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Wishlist)