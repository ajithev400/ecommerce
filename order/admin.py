from django.contrib import admin
from django.db import models

from order.models import Order, OrderProduct, Payment

# Register your models here.
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "full_name", "phone", "is_ordered"]
    list_filter = ["status", "is_ordered"]
    search_field = [
        "order_number",
        "first_name",
        "last_name",
        "phone",
        "email",
    ]
    list_per_page = 20
    inlines = [OrderProductInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)
