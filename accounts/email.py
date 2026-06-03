from threading import Thread

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from .tokens import make_email_confirmation_token


def send_confirmation_email_async(request, user):
    token = make_email_confirmation_token(user)
    confirm_url = request.build_absolute_uri(
        reverse("accounts:confirm_email", kwargs={"token": token})
    )
    subject = "Подтверждение регистрации"
    message = render_to_string(
        "accounts/email_confirmation.txt",
        {"user": user, "confirm_url": confirm_url},
    )

    def task():
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    Thread(target=task, daemon=True).start()
