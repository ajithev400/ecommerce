from django.db import models
from django.db.models.aggregates import Sum
from django.utils import timezone
from account.models import Account
from category.models import category,sub_category
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Avg, Count
from django.apps import apps


class product(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    # vender =
    product_name = models.CharField(max_length=100, null=False)
    slug = models.SlugField(max_length=100,unique=True)  
    image = models.ImageField(upload_to="photos/product", null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    margin_price = models.IntegerField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    stock = models.IntegerField(null=True,blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated_at','-created_at']

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name, self.category.category_name)
        super(product, self).save(*args, **kwargs)

    # def averageReview(self):
    #     reviews = ReviewRating.objects.filter(
    #         product=self, status=True
    #     ).aggregate(average=Avg("rating"))
    #     avg = 0
    #     if reviews["average"] is not None:
    #         avg = float(reviews["average"])
    #     return avg

    # def countReview(self):
    #     reviews = ReviewRating.objects.filter(
    #         product=self, status=True
    #     ).aggregate(count=Count("id"))
    #     count = 0
    #     if reviews["count"] is not None:
    #         count = int(reviews["count"])
    #     return count
    
    # def get_revenue(self, month=timezone.now().month):
    #     orderproduct = apps.get_model("order", "OrderProduct")
    #     order = orderproduct.objects.filter(
    #         product=self, created_at__month=month, status="Delivered"
    #     )
    #     return order.values("product").annotate(revenue=Sum("price"))

class VarientColor(models.Model):
    color_name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.color_name



        
class Variation(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE, related_name="varion")
    varient_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    sub_category = models.ForeignKey(sub_category, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(VarientColor, on_delete=models.CASCADE,null=True,blank=True)
    size = models.ForeignKey('VarientSize',on_delete=models.CASCADE,null=True,blank=True )
    image1 = models.ImageField(upload_to="photos/product", blank=True)
    image2 = models.ImageField(upload_to="photos/product", blank=True)
    image3 = models.ImageField(upload_to="photos/product", blank=True)
    image4 = models.ImageField(upload_to="photos/product", blank=True)
    # stock = models.IntegerField(null=True,blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.varient_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.varient_name,self.color)
        super(Variation, self).save(*args, **kwargs)
    
    def get_url(self):
        return reverse(
        "product_details",
        args=[self.product.slug, self.slug],
    )

class VarientSize(models.Model):

    product = models.ForeignKey(Variation, on_delete=models.CASCADE,blank=True,null=True)
    size = models.IntegerField(blank=True,null=True)
    stock = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.size)
    

class ReviewRating(models.Model):
    varient = models.ForeignKey(Variation, on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
    def rating_percentage(self):
        return self.rating * 20


# class Banners(models.Model):
#     vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100, null=True)
