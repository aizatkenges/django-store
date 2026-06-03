from .cart import Cart


def cart_summary(request):
    return {"cart_items_count": len(Cart(request))}
