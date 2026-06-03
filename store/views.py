from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import AddToCartForm, CheckoutForm
from .models import OrderItem, Product


def product_list(request):
    products = Product.objects.all()
    return render(request, "store/product_list.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(
        request,
        "store/product_detail.html",
        {"product": product, "form": AddToCartForm()},
    )


def cart_detail(request):
    cart = Cart(request)
    return render(request, "store/cart_detail.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = AddToCartForm(request.POST)
    if form.is_valid():
        Cart(request).add(product, form.cleaned_data["quantity"])
        messages.success(request, f"Товар «{product.name}» добавлен в корзину.")
        if request.POST.get("next") == "checkout":
            return redirect("store:checkout")
    return redirect("store:cart_detail")


@require_POST
def cart_update(request, product_id):
    quantity = request.POST.get("quantity", 1)
    Cart(request).update(product_id, quantity)
    messages.success(request, "Корзина обновлена.")
    return redirect("store:cart_detail")


@require_POST
def cart_remove(request, product_id):
    Cart(request).remove(product_id)
    messages.success(request, "Товар удален из корзины.")
    return redirect("store:cart_detail")


@require_POST
def cart_clear(request):
    Cart(request).clear()
    messages.success(request, "Корзина очищена.")
    return redirect("store:cart_detail")


def checkout(request):
    cart = Cart(request)
    if cart.is_empty:
        messages.info(request, "Добавьте товары в корзину перед оформлением заказа.")
        return redirect("store:product_list")

    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                )
        cart.clear()
        return redirect("store:order_success", order_id=order.id)

    return render(request, "store/checkout.html", {"cart": cart, "form": form})


def order_success(request, order_id):
    return render(request, "store/order_success.html", {"order_id": order_id})
