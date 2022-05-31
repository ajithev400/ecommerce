from tkinter import N
from django.urls import path
from . import views


urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin-logout/',views.admin_logout,name='admin_logout'),

    path('add-product/',views.add_product,name='add_product'),
    path('add-variant/<str:pk>/',views.add_verient,name='add_variant'),
    path('delete-product/<str:pk>/',views.delete_product,name='delete_product'),

    path('edit-product/<str:pk>/',views.edit_product,name='edit_product'),
    path('edit-variant/<str:pk>/',views.edit_variant,name='edit_variant'),

    path('list-product/',views.list_product,name='list_product'),
    path('view-product/<str:pk>/',views.view_product,name='view-product'),

    path('activate-product/<str:pk>/',views.activate_product,name='activate_product'),

    path('customers/',views.customers,name='customers'),
    path('customer_pickoff/<str:pk>',views.customer_pickoff,name='customer_pickoff'),
]   