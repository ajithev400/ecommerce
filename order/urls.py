from django.urls import path
from .import views

urlpatterns = [
    path('',views.place_order,name='place_order'),
    path('payments/',views.payment,name='payment'),
    path('paymenthandler/',views.paymenthandler,name='paymenthandler'),
    path('order-complete/',views.order_complete,name='order_complete'),
    path('cash-on-delivery/',views.cash_on_delivery,name='cash_on_delivery')
      
]