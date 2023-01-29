from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from.models import Product
from django.db.models import Q

from category.models import Category

# Create your views here.
    
def store(request,category_slug=None):
    if category_slug!=None:
        categories=Category.objects.get(slug=category_slug)
        products=Product.objects.filter(category=categories)
        paginator=Paginator(products,3)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()   
    else:
        
        products=Product.objects.filter(is_available=True)
        paginator=Paginator(products,3)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
    context={
        "products":paged_products,
        'product_count':product_count,
    }

    return render (request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
    context={
        'single_product':single_product,
    }
    
    return render (request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET.get('keyword')
        if keyword:
            products=Product.objects.filter(Q(disc__icontains=keyword) |Q(product_name__icontains=keyword))
            product_count=products.count()
            context={
                'products':products,
                'product_count':product_count
            }
        else:
            return redirect('store')
            
    return render(request,'store/store.html',context)    

