from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .tokens import make_email_confirmation_token


class EmailAuthTests(TestCase):
    def test_register_creates_inactive_user_and_sends_email_in_background(self):
        with patch("accounts.views.send_confirmation_email_async") as send_email:
            response = self.client.post(
                reverse("accounts:register"),
                {
                    "username": "buyer",
                    "email": "buyer@example.com",
                    "password1": "StrongPass123!",
                    "password2": "StrongPass123!",
                },
            )

        user = get_user_model().objects.get(username="buyer")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(user.is_active)
        self.assertEqual(user.email, "buyer@example.com")
        send_email.assert_called_once()

    def test_user_can_confirm_email_and_login(self):
        user = get_user_model().objects.create_user(
            username="buyer",
            email="buyer@example.com",
            password="StrongPass123!",
            is_active=False,
        )
        token = make_email_confirmation_token(user)

        response = self.client.get(reverse("accounts:confirm_email", args=[token]))
        user.refresh_from_db()

        self.assertRedirects(response, reverse("store:product_list"))
        self.assertTrue(user.is_active)
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.id)

    def test_inactive_user_cannot_login_before_confirmation(self):
        get_user_model().objects.create_user(
            username="buyer",
            email="buyer@example.com",
            password="StrongPass123!",
            is_active=False,
        )

        response = self.client.post(
            reverse("accounts:login"),
            {"username": "buyer", "password": "StrongPass123!"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
