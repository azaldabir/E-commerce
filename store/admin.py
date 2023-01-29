from django.contrib import admin
from .models import Product,Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ['product_name','slug','price','disc','stock','image']
admin.site.register(Product,ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display=['product','variation_category','is_active']
    list_editable=["is_active"]
    
admin.site.register(Variation,VariationAdmin)
