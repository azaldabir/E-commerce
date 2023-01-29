from django.db import models
from store.models import Product,Variation

# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField( max_length=500)
    date_add=models.DateField( auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

    
    
class Cart_item(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    variation=models.ManyToManyField(Variation,blank=True)

    def sub_total(self):
        return self.product.price*self.quantity
    
    
    
    
  

