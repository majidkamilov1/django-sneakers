
from .models import Cart

def cart_items_processor(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
    else:
        cart_items = []
    
    return {
        'cart   _items': cart_items
    }
