from django.shortcuts import render,redirect
from django.http import HttpResponse
from store.models import Product,Variation
from .models import Cart,Cart_item

# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


def cart(request):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_items=Cart_item.objects.filter(cart=cart)
    total=0
    tax=0
    grand_total=0
    quantity=0
    for cart_item in cart_items:
        total=total+cart_item.product.price*cart_item.quantity
        quantity=cart_item.quantity+quantity
        tax=(total*8)/100
        grand_total=total+tax
    context={
        'cart_items':cart_items,
        'total':total,
        'tax':tax,
        'grand_total':grand_total,
        'quantity':quantity,
    }
    return render(request,"cart/cart.html",context)

    


# def add_cart(request,product_id):  
#     product=Product.objects.get(id=product_id)
#     try:
#         cart=Cart.objects.get(cart_id=_cart_id(request))
#     except Cart.DoesNotExist:
#         cart=Cart.objects.create(
#             cart_id =_cart_id(request)
#             )


#     try:
#         cart_item=Cart_item.objects.get(cart=cart,product=product)
#         cart_item.quantity+=1
    
#     except Cart_item.DoesNotExist:
#         cart_item=Cart_item.objects.create(

#             product=product,
#             cart=cart,
#             quantity=1
#         )
#     cart.save()
#     cart_item.save()

#     return redirect('cart')

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    product_variation=[]
    
    if request.method=="POST":
        for item in request.POST:
            key=item
            value=request.POST[key]
            try: #this try for fetching variation
                variation=Variation.objects.get( product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)

            except:
                pass
                   
    
    try:#this try for fetch cart
        cart=Cart.objects.get(cart_id=_cart_id(request))
    
    except:
        cart=Cart.objects.create(cart_id=_cart_id(request))
    cart.save()


    is_cart_item_exist=Cart_item.objects.filter(cart=cart,product=product).exists()
    if is_cart_item_exist:#this  for cart item returns true or false
        cart_item=Cart_item.objects.filter(product=product, cart=cart)
            # existing variation
            #current variation--> product variation
            #item id

        ex_var_list=[]
        id=[]
        for item in cart_item:
            existing_variation=item.variation.all()
            ex_var_list.append( list(existing_variation) )
            id.append(item.id)
    # cart_item.quantity=cart_item.quantity + 1

        if product_variation in ex_var_list:
            index=ex_var_list.index(product_variation)
            item_id=id[index]
            item=Cart_item.objects.get(product=product,id=item_id)
            item.quantity+=1
            item.save()
        else:
            item=Cart_item.objects.create(product=product,quantity=1, cart=cart)        
            if len(product_variation)>0:
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()

    else:
        cart_item=Cart_item.objects.create(cart=cart,product=product,quantity=1)
        
        if len(product_variation)>0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)
        cart_item.save()
    
    return redirect("cart")
    


def remove_cart(request,product_id,cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=Product.objects.get(id=product_id)

    try:
        cart_item=Cart_item.objects.get(cart=cart,product=product,id=cart_item_id)
        if cart_item.quantity>1:
            cart_item.quantity=cart_item.quantity-1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
        
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):

    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_item=Cart_item.objects.get(cart=cart,product=product_id,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
