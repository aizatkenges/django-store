# Django Store

Простой интернет-магазин на Django с серверным рендерингом через Django Templates.

## Запуск

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```text
http://localhost:8000
```

При старте контейнер автоматически выполняет миграции, загружает демо-товары и собирает статические файлы.

## Административная панель

Админка доступна по адресу:

```text
http://localhost:8000/admin/
```

Чтобы создать администратора локально:

```bash
docker compose exec web python manage.py createsuperuser
```

В админке можно создавать, редактировать и удалять товары, а также просматривать заказы и позиции заказов.

## Регистрация и подтверждение email

Пользователь может зарегистрироваться по адресу:

```text
http://localhost:8000/accounts/register/
```

После регистрации аккаунт создается неактивным. Приложение отправляет письмо со ссылкой подтверждения email в фоновой задаче через отдельный поток.

Для реальной SMTP-отправки через Gmail создайте файл `.env` рядом с `docker-compose.yml`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

`EMAIL_HOST_PASSWORD` - это не обычный пароль от Gmail, а Google App Password. Его можно создать в Google Account после включения двухэтапной проверки.

Пример файла лежит в `.env.example`.

## Тесты

```bash
python manage.py test
```

Или внутри Docker:

```bash
docker compose exec web python manage.py test
```

## Архитектура

Проект состоит из одного Django-приложения `store`.

- `Product` хранит название, описание, цену и изображение товара.
- `Order` хранит имя клиента, номер телефона и дату создания заказа.
- `OrderItem` связывает заказ с товарами и количеством.
- Корзина хранится в Django session, поэтому пользователь может добавлять товары до оформления заказа без авторизации.
- При оформлении заказа данные сохраняются транзакционно: создается `Order`, затем связанные `OrderItem`.
- Django Admin используется как административная панель для управления товарами и просмотра заказов.
- Приложение `accounts` отвечает за регистрацию, вход, выход и подтверждение email.

## Используемые технологии

- Python 3.12
- Django 5
- Django Templates
- SQLite
- Docker Compose
- Pillow для работы с изображениями товаров

## Основные маршруты

- `/` - каталог товаров
- `/products/<id>/` - карточка товара
- `/cart/` - корзина
- `/checkout/` - оформление заказа
- `/accounts/register/` - регистрация
- `/accounts/login/` - вход
- `/admin/` - административная панель
