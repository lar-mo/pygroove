from .models import Cart

def cart_count(request):
    """Add cart item count to all template contexts"""
    cookie_id = request.COOKIES.get('cart_id')
    count = 0
    
    if cookie_id:
        try:
            cart = Cart.objects.get(cookie_id=cookie_id)
            count = cart.items.count()
        except Cart.DoesNotExist:
            count = 0
    
    return {'cart_item_count': count}
