from django.core import signing


EMAIL_CONFIRMATION_SALT = "accounts.email-confirmation"


def make_email_confirmation_token(user):
    return signing.dumps({"user_id": user.id}, salt=EMAIL_CONFIRMATION_SALT)


def read_email_confirmation_token(token, max_age=60 * 60 * 24):
    return signing.loads(token, salt=EMAIL_CONFIRMATION_SALT, max_age=max_age)
