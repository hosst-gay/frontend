import secrets


def user_id():
    return secrets.token_urlsafe(10)