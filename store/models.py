from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.
class Product(models.Model):

    product_name=models.CharField(max_length=50)
    slug=models.SlugField()
    price=models.IntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    stock=models.IntegerField()
    disc=models.TextField()
    image=models.ImageField(upload_to='photos/product')

    is_available = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)


    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
        
    def __str__(self):
        return self.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category="color", is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category="size", is_active=True)
        


variation_category_choices={

    ("color" ,"color"),
    ("size", "size"),
}

class Variation(models.Model):
    product=models.ForeignKey( Product , on_delete=models.CASCADE)
    variation_category=models.CharField( max_length=50, choices=variation_category_choices)
    variation_value=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    objects=VariationManager()
    
    def __str__(self):
        return self.variation_value
    

