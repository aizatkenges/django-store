from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Цена")),
                ("image", models.ImageField(blank=True, upload_to="products/", verbose_name="Изображение")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(max_length=255, verbose_name="Имя клиента")),
                ("phone_number", models.CharField(max_length=32, verbose_name="Номер телефона")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(default=1, verbose_name="Количество")),
                (
                    "order",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="store.order"),
                ),
                (
                    "product",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="order_items", to="store.product"),
                ),
            ],
            options={
                "verbose_name": "Позиция заказа",
                "verbose_name_plural": "Позиции заказа",
            },
        ),
    ]
