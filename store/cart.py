from decimal import Decimal

from .models import Product


CART_SESSION_KEY = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(CART_SESSION_KEY, {})

    def add(self, product, quantity=1):
        product_id = str(product.id)
        current = self.cart.get(product_id, 0)
        self.cart[product_id] = current + int(quantity)
        self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        quantity = int(quantity)
        if quantity > 0:
            self.cart[product_id] = quantity
        else:
            self.cart.pop(product_id, None)
        self.save()

    def remove(self, product_id):
        self.cart.pop(str(product_id), None)
        self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.cart = self.session[CART_SESSION_KEY]
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(product.id): product for product in products}

        for product_id, quantity in self.cart.items():
            product = product_map.get(product_id)
            if not product:
                continue
            total_price = product.price * quantity
            yield {
                "product": product,
                "quantity": quantity,
                "total_price": total_price,
            }

    def __len__(self):
        return sum(self.cart.values())

    @property
    def total_price(self):
        total = Decimal("0.00")
        for item in self:
            total += item["total_price"]
        return total

    @property
    def is_empty(self):
        return len(self) == 0
