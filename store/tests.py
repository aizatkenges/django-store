from django.test import TestCase
from django.urls import reverse

from .models import Order, OrderItem, Product


class StoreViewsTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test product",
            description="Product description",
            price="1200.00",
        )

    def test_product_list_displays_products(self):
        response = self.client.get(reverse("store:product_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, "1200")

    def test_product_detail_displays_product(self):
        response = self.client.get(reverse("store:product_detail", args=[self.product.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.description)

    def test_create_order_from_cart(self):
        self.client.post(
            reverse("store:cart_add", args=[self.product.id]),
            {"quantity": 2},
        )

        response = self.client.post(
            reverse("store:checkout"),
            {"customer_name": "Aizat", "phone_number": "+7 777 123 45 67"},
        )

        order = Order.objects.get()
        order_item = OrderItem.objects.get(order=order)

        self.assertRedirects(response, reverse("store:order_success", args=[order.id]))
        self.assertEqual(order.customer_name, "Aizat")
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 2)

    def test_checkout_requires_non_empty_cart(self):
        response = self.client.get(reverse("store:checkout"))

        self.assertRedirects(response, reverse("store:product_list"))
