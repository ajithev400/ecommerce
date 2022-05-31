from django.db import models

from account.models import Account
from category.models import category,sub_category
from django.urls import reverse
from django.utils.text import slugify

class product(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    sub_category = models.ManyToManyField(sub_category)
    # vender =
    product_name = models.CharField(max_length=100, null=False)
    slug = models.SlugField(max_length=100,unique=True)  
    image = models.ImageField(upload_to="photos/product", null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    margin_price = models.IntegerField(default=5000)
    price = models.IntegerField(default=5000)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at','-created_at']

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(product, self).save(*args, **kwargs)

    

class VarientColor(models.Model):
    color_name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.color_name



        
class Variation(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE, related_name="varion")
    varient_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    color = models.ForeignKey(VarientColor, on_delete=models.CASCADE,null=True,blank=True)
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
    
    # def get_url(self):
    #     return reverse(
    #         "product-detail",
    #         args=[self.product.slug, self.slug],           
    #     )
    def get_url(self):
        return reverse(
        "product-detail",
        args=[self.product.slug, self.slug],
    )

class VarientSize(models.Model):
    product = models.ManyToManyField(Variation)
    size = models.IntegerField()
    stock = models.IntegerField()
    

class ReviewRating(models.Model):
    varient = models.ForeignKey(Variation, on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    # ip = models.CharField(max_length=20, null=True ,blank=True)
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
