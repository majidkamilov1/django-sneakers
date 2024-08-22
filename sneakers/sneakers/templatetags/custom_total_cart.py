from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def total_price(context):
    cart_items = context.get('cart_items', [])
    if not cart_items:
        return 0
    result = sum(item.sneaker.price * item.quantity for item in cart_items)
    return result
