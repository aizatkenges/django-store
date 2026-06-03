from django import forms

from .models import Order


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Количество",
        widget=forms.NumberInput(attrs={"class": "input input--qty"}),
    )


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("customer_name", "email", "phone_number", "address", "city", "postal_code")
        labels = {
            "customer_name": "Имя",
            "email": "Email",
            "phone_number": "Телефон",
            "address": "Адрес",
            "city": "Город",
            "postal_code": "Индекс",
        }
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "input", "placeholder": "Введите ваше имя"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "Введите ваш email"}),
            "phone_number": forms.TextInput(attrs={"class": "input", "placeholder": "Введите ваш телефон"}),
            "address": forms.TextInput(attrs={"class": "input", "placeholder": "Улица, дом, квартира"}),
            "city": forms.TextInput(attrs={"class": "input", "placeholder": "Введите город"}),
            "postal_code": forms.TextInput(attrs={"class": "input", "placeholder": "Почтовый индекс"}),
        }
