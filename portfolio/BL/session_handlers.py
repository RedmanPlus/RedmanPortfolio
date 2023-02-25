import secrets


def create_session_key():

    return secrets.token_urlsafe(32)


def create_email_token():

    return secrets.token_urlsafe(16)
