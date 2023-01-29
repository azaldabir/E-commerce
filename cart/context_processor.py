from django.urls import path
from .models import Cart,Cart_item
from .views import _cart_id

def counter(request):
    if "admin" in request.path:
        return{}
    else:
        cart_count=0
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(request))
            cart_items=Cart_item.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count=cart_count + cart_item.quantity

        except Cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count)
