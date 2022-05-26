from audioop import reverse
from django.db import models


# Create your models here.
class category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    # cat_image = models.ImageField(upload_to="photos/categories",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "category"
        verbose_name_plural = "categories"
    def __str__(self):
        return self.category_name
    
    def get_url(self):
        return reverse('product_by_category',args=[self.slug])

class sub_category(models.Model):
    category = models.ManyToManyField(category,blank=True)
    sub_category_name = models.CharField(max_length=100,db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "sub_category"
        verbose_name_plural = "sub_categories"

    def __str__(self):
        return self.sub_category_name