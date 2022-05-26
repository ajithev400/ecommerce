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

    path('product-detail/<str:pk>/',views.product_details,name='product_details'),

]