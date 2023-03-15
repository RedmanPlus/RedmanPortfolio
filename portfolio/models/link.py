from pydantic import HttpUrl

from portfolio.models.core import ORMModel


class LinkInfo(ORMModel):
    resource: str
    url: HttpUrl
