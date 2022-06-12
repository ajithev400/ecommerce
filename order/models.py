from operator import mod
from django.db import models
from account.models import Account
from store.models import Variation,product

STATUS1 = (
    ("New", "New"),
    ("Placed", "Placed"),
    ("Shipped", "Shipped"),
    ("Accepted", "Accepted"),
    ("Delivered", "Delivered"),
    ("Canceled", "Canceled"),
)
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    Payment_id = models.CharField(max_length=100)
    Payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Payment_id


class Order(models.Model):
    STATUS =(
        ("New","New"),
        ("Accepted","Accepted"),
        ("Completed","Completed"),
        ("Cancelled","Cancelled"),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    Payment = models.ForeignKey(Payment, on_delete=models.CASCADE,blank=True,null=True)
    order_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    order_note = models.CharField(max_length=200, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(choices=STATUS, max_length=20, default="New")
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def full_address(self):
        return f"{self.address1} {self.address2}"

    def __str__(self):
        return self.first_name



class OrderProduct(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS1, max_length=20, default="New")
    products = models.ForeignKey(product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    text = models.CharField(max_length=100, blank=True)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.products.product_name

    def sub_total(self):
        return self.quantity * self.price

    def varient_tax(self):
        return self.sub_total() * 2 / 100

    def grand_total(self):
        return self.sub_total() + self.varient_tax()