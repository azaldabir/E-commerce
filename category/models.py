
from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name=models.CharField( max_length=50)
    slug=models.SlugField()
    disc=models.TextField()
    cat_image=models.ImageField(upload_to='photos/category')
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.category_name
    
    def get_url(self):
        return reverse('product_by_category', args=[self.slug])
    
    

