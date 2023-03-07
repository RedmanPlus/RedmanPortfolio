from miniopy_async import Minio

from portfolio.settings import MINIO_ACCESS_KEY, MINIO_SECRET_KEY


def get_minio():
    yield Minio(
        "127.0.0.1:9000",
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
