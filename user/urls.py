from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_user,name='login'),
    path('register/',views.user_register,name='register'),
    path('register-otp/',views.register_otp,name='register_otp'),
    path('logout/',views.logout_user,name='logout'),

    path('product-detail/<slug:product_slug>/<slug:variant_slug>/',views.product_details,name='product_details'),
    path('my-address/',views.user_address,name='user_address'),
    path('my-profile/',views.user_profile,name='user_profile'),

    path('my-orders/',views.user_orders,name='user_orders'),
    path('order-detail/<str:order_id>/',views.order_detail,name='order_detail'),

]