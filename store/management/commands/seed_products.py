from django.core.management.base import BaseCommand

from store.models import Product


class Command(BaseCommand):
    help = "Creates demo products for local development."

    def handle(self, *args, **options):
        products = [
            {
                "name": "Ноутбук Lenovo",
                "description": "IdeaPad 1 15IJL7 15.6 / 8 ГБ / SSD 512 ГБ / Win 11 Pro",
                "short_specs": "IdeaPad 1 15IJL7",
                "price": "21440.00",
                "badge": "Новинка",
                "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Смартфон Samsung Galaxy A54",
                "description": "6.4 / 8 ГБ / 128 ГБ / 5G / Black",
                "short_specs": "8 ГБ / 128 ГБ",
                "price": "149990.00",
                "badge": "Хит продаж",
                "image_url": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-a54-1.jpg",
            },
            {
                "name": "Наушники Apple AirPods Max",
                "description": "Беспроводные / Серебристые",
                "short_specs": "Беспроводные / Серебристые",
                "price": "229990.00",
                "badge": "Акция",
                "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=900&q=80",
            },
        ]

        Product.objects.filter(
            name__in=[
                "Ноутбук Atlas 14",
                "Смартфон Nova X",
                "Наушники Wave Pro",
                "Умные часы Pulse",
            ]
        ).delete()

        for data in products:
            Product.objects.update_or_create(name=data["name"], defaults=data)

        self.stdout.write(self.style.SUCCESS("Demo products are ready."))
