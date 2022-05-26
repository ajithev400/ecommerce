from django.db import models

from account.models import Account
from category.models import category,sub_category
from django.urls import reverse
from django.urls import reverse

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
    

    def get_url(self):
        return reverse(
        "product_detail",
        args=[self.product.category.slug, self.product.slug, self.slug],
    )

class VarientColor(models.Model):
    color_name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.color_name

# class VarientSize(models.Model):
#     product = models.ManyToManyField()
#     size = models.IntegerField()
    

#     def __str__(self):
#         return self.color_name

SIZE_CHOICE = (
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
    ("13", "13"),
    ("14", "14"),
    ("15", "15"),
)

        
class Variation(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE, related_name="varion")
    varient_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    color = models.ForeignKey(VarientColor, on_delete=models.CASCADE,null=True,blank=True)
    size  = models.CharField(choices=SIZE_CHOICE,max_length=20,default="5")
    image1 = models.ImageField(upload_to="photos/product", blank=True)
    image2 = models.ImageField(upload_to="photos/product", blank=True)
    image3 = models.ImageField(upload_to="photos/product", blank=True)
    image4 = models.ImageField(upload_to="photos/product", blank=True)
    margin_price = models.IntegerField()
    price = models.IntegerField(null=True,blank=True)
    stock = models.IntegerField(null=True,blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.varient_name
    
    def get_url(self):
        return reverse(
            "product_detail",
            args=[self.product.category.slug, self.slug],
        )

# class Size(models.Model):
#     product = models.ForeignKey(Variation,on_delete=models.CASCADE)
#     size = models.IntegerField()
    

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
