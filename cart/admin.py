from django.contrib import admin
from .models import Cart,Cart_item
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display=['cart_id','date_add']

class CartItemAdmin(admin.ModelAdmin):
    list_display=['product','cart','quantity','is_active']
admin.site.register(Cart,CartAdmin)
admin.site.register(Cart_item,CartItemAdmin)