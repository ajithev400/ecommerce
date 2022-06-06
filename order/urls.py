from django.urls import path
from .import views

urlpatterns = [
    path('',views.place_order,name='place_order'),
    path('payments/',views.payment,name='payment'),
    path('paymenthandler/',views.paymenthandler,name='paymenthandler'),

      
]