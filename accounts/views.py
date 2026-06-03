from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.core import signing
from django.shortcuts import redirect, render

from .email import send_confirmation_email_async
from .forms import RegisterForm
from .tokens import read_email_confirmation_token


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.email = form.cleaned_data["email"]
        user.is_active = False
        user.save()
        send_confirmation_email_async(request, user)
        return render(request, "accounts/registration_pending.html", {"email": user.email})

    return render(request, "accounts/register.html", {"form": form})


def confirm_email(request, token):
    try:
        data = read_email_confirmation_token(token)
    except signing.BadSignature:
        messages.error(request, "Ссылка подтверждения недействительна или устарела.")
        return redirect("accounts:login")

    User = get_user_model()
    try:
        user = User.objects.get(id=data["user_id"])
    except User.DoesNotExist:
        messages.error(request, "Пользователь не найден.")
        return redirect("accounts:login")

    user.is_active = True
    user.save(update_fields=["is_active"])
    login(request, user)
    messages.success(request, "Email подтвержден. Вы вошли в аккаунт.")
    return redirect("store:product_list")
