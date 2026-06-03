from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="badge",
            field=models.CharField(blank=True, max_length=32, verbose_name="Бейдж"),
        ),
        migrations.AddField(
            model_name="product",
            name="image_url",
            field=models.URLField(blank=True, verbose_name="Ссылка на изображение"),
        ),
        migrations.AddField(
            model_name="product",
            name="short_specs",
            field=models.CharField(blank=True, max_length=255, verbose_name="Краткие характеристики"),
        ),
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.CharField(blank=True, max_length=255, verbose_name="Адрес"),
        ),
        migrations.AddField(
            model_name="order",
            name="city",
            field=models.CharField(blank=True, max_length=120, verbose_name="Город"),
        ),
        migrations.AddField(
            model_name="order",
            name="email",
            field=models.EmailField(blank=True, max_length=254, verbose_name="Email"),
        ),
        migrations.AddField(
            model_name="order",
            name="postal_code",
            field=models.CharField(blank=True, max_length=32, verbose_name="Индекс"),
        ),
    ]
