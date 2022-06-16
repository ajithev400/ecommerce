
from django.db import models
from account.models import Account
from store.models import Variation,product,VarientSize

class Cart(models.Model):
    cart_id = models.CharField(max_length=60,null=True,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItems(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True,blank=True)
    varient = models.ForeignKey(Variation, on_delete=models.CASCADE)
    Cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField()
    size = models.ForeignKey(VarientSize,on_delete=models.CASCADE,null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def total(self):
        return self.varient.product.price * self.quantity
    
    def __unicode__(self):
        return self.varient
    
    def sub_total(self):
        return self.varient.product.price * self.quantity



class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    varient = models.ForeignKey(Variation, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.varient.varient_name
