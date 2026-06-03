from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField("Изображение", upload_to="products/", blank=True)
    image_url = models.URLField("Ссылка на изображение", blank=True)
    badge = models.CharField("Бейдж", max_length=32, blank=True)
    short_specs = models.CharField("Краткие характеристики", max_length=255, blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={"pk": self.pk})

    @property
    def image_src(self):
        if self.image:
            return self.image.url
        return self.image_url


class Order(models.Model):
    customer_name = models.CharField("Имя клиента", max_length=255)
    email = models.EmailField("Email", blank=True)
    phone_number = models.CharField("Номер телефона", max_length=32)
    address = models.CharField("Адрес", max_length=255, blank=True)
    city = models.CharField("Город", max_length=120, blank=True)
    postal_code = models.CharField("Индекс", max_length=32, blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.pk} от {self.customer_name}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.select_related("product"))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
