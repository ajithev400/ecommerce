from django.urls import path
from .import views

urlpatterns = [
    path('',views.cart,name='cart'),
    # path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),
    path("add_cart/", views.add_cart, name="add_cart"),
    path('delete_cart/<int:product_id>/',views.delete_cart,name='delete_cart'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name='remove_cart'),
    path('update-cart/<str:product_id>/',views.update_cart,name='update_cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('addtowishlist/',views.add_wishlist,name='addtowishlist'),
]