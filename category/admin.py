from django.contrib import admin

from .models import category,sub_category

class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}
    list_display = ("category_name", "slug")


class sub_categoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("sub_category_name",)}
    list_display = ("sub_category_name", "slug")


class varientsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("varient_name",)}
    list_display = ("varient_name", "slug")


admin.site.register(category, categoryAdmin)
admin.site.register(sub_category, sub_categoryAdmin)
