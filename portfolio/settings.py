import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig

load_dotenv()

REAL_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres"

mail_conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("SMTP_MAIL"),
    MAIL_PASSWORD = os.getenv("SMTP_PASSWORD"),
    MAIL_FROM = os.getenv("SMTP_MAIL"),
    MAIL_PORT = os.getenv("SMTP_PORT"),
    MAIL_SERVER = os.getenv("SMTP_SERVER"),
    MAIL_FROM_NAME = "RedmanPortfolio",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
