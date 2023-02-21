import secrets


def create_session_key():

    return secrets.token_urlsafe(32)
