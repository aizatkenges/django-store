from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Имя пользователя",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "input"

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email
